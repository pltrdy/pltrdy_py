#!/usr/bin/env python
import os

from pltrdy.rouge import read_rouge
from pltrdy.wc import wordcount


def srcrougefct(x):
    if x["src_rouge"] == "none":
        return 0.0
    else:
        return -float(x["src_rouge"].split(";")[0])


def perplexity(rouge_path, incl_oov=True):
    n_line = 0 if incl_oov else 1

    ppl_path = rouge_path.replace("rouge", "ppl")
    with open(ppl_path) as f:
        lines = [_.strip() for _ in f]
    line = lines[n_line]
    ppl = line.split("OOVs:")[-1]
    ppl = float(ppl)
    return ppl


def clean_suffix(suffix):
    to_remove = ["bpe", "decoded", "rouge"]
    for r in to_remove:
        suffix = suffix.replace(r, "")
    return suffix


class ResultsExplorer(object):
    DEFAULT_FIELDS = [
        'exp', 'model', 'step', 'dec_suffix',
        'wc', 'rouge_1', 'rouge_2', 'rouge_l', 'src_rouge'
    ]

    FILTERS = {
        "valid": lambda p: ".valid" in p,
        "predtok": lambda p: "predtok" in p,
        "onlytoks": lambda p: "onlytoks" in p,
    }

    SORT_FCT = {
        "copy_desc": srcrougefct,
        "ppl": lambda x: -x["ppl"]
    }

    def __init__(self, name, exps=[], exps_with_regex={},
                 custom_filters={}, extra_fields={}):
        """
            name:
            exps: list of directories where *.rouge files are
            exps_with_regex: dict of `directory: regex`
            custom_filters: dict of filters `name: filter function`
            extra_fields: dict of `name: field function` that take a .rouge
                          path and should return the field value

        """
        self.name = name

        self.exps_with_regex = exps_with_regex
        self.exps_with_regex.update({
            e: r"model(.*)\.rouge"
            for e in exps
        })
        self.extra_fields = extra_fields
        self.filters = dict(ResultsExplorer.FILTERS)
        self.filters.update(custom_filters)

    def all_filters(self, path, filters_switch):
        for k, v in filters_switch.items():
            _v = self.filters[k](path)
            print(path, k, v, _v)
            if not v == _v:
                return False
        return True
        return all([
            self.filters[k](path) == v
            for k, v in filters_switch.items()
        ])

    def explore_results(self, sort_field=None, **filters):
        import re
        results = []
        fields = ResultsExplorer.DEFAULT_FIELDS
        fields.extend(self.extra_fields.keys())

        for exp_root, reg in self.exps_with_regex.items():
            print(exp_root)
            exp_results = sorted([
                _ for _ in os.listdir(exp_root)
                if re.match(reg, _) is not None
                and self.all_filters(_, filters)
            ])
            for result_name in exp_results:
                rouge_path = os.path.join(exp_root, result_name)

                with open(rouge_path, 'r') as f:
                    lines = [_.strip() for _ in f]

                if not len(lines) == 13:
                    print("Incorrect result files (%d != 13 lines) %s" %
                          (len(lines), rouge_path))
                    continue

                model = result_name.split("_pred.")[0]
                try:
                    step = result_name.split("_pred.")[1].split("k")[0]
                except IndexError:
                    print("Cannot read step of '%s'" % rouge_path)
                    raise

                try:
                    float(step)
                except BaseException:
                    continue
                src_rouge_path = rouge_path.replace('.rouge', '.src_rouge')
                if os.path.exists(src_rouge_path):
                    try:
                        r = read_rouge(src_rouge_path)
                        src_rouge = " ; ".join([
                            "%2.2f" % (100 * float(r["rouge-1"][k]))
                            for k in ["r", "p", "f"]
                        ])
                    except BaseException:
                        src_rouge = "err"
                else:
                    src_rouge = "none"
                r = {}
                dec_suffix = rouge_path.split(str(step) + "k")[1]\
                    .split(".txt")[0]\
                    .replace('.', '')\
                    .replace('true_test', '')
                r['dec_suffix'] = clean_suffix(dec_suffix)
                r['path'] = rouge_path
                r['exp'] = exp_root
                r['model'] = model
                r['step'] = step
                r['rouge_1'] = float(lines[3].split(
                    'Average_F: ')[1].split()[0])
                r['rouge_2'] = float(lines[7].split(
                    'Average_F: ')[1].split()[0])
                r['rouge_l'] = float(lines[11].split(
                    'Average_F: ')[1].split()[0])
                r['src_rouge'] = src_rouge
                try:
                    wc = int(wordcount(rouge_path.replace('.rouge', '')))
                except Exception:
                    wc = -1
                    raise
                r['wc'] = wc

                for k, f in self.extra_fields.items():
                    r[k] = f(rouge_path)
                print(r)
                results.append(r)

        if sort_field is None:
            results = sorted(results,
                             key=lambda x: (
                                 x['rouge_1'],
                                 x['exp'],
                                 x['model'],
                                 x['step']
                             ),
                             reverse=True)
        else:
            if sort_field in ResultsExplorer.SORT_FCT:
                sort_fct = ResultsExplorer.SORT_FCT[sort_field]
            else:
                def sort_fct(x): return x[sort_field]
            results = sorted(results,
                             key=lambda x: (
                                 sort_fct(x),
                                 x['rouge_1'],
                                 x['exp'],
                                 x['model'],
                                 int(x['step'].replace('k', ''))
                             ),
                             reverse=True)

        assert len(results) > 0
        m = ["| " + "|  ".join(fields) + " |"]
        m += ["|---" * len(fields) + " |"]

        top = {k: max([r[k] for r in results])
               for k in ['rouge_1', 'rouge_2', 'rouge_l', 'wc']}
        for r in results:
            for k in ['rouge_1', 'rouge_2', 'rouge_l', 'wc']:
                if r[k] == top[k]:
                    r[k] = "**%f**" % r[k]

            _r = "| " + "| ".join([str(r[k]).replace('_', '_')
                                   for k in fields])
            _r += " |"
            m += [_r]

        filters_suffix = ""
        for k, v in filters.items():
            if v:
                filters_suffix += ".%s" % k

        sort_suffix = "" if sort_field is None else ".%s" % sort_field
        out_path = "results.%s%s%s.md" % (
            self.name, filters_suffix, sort_suffix)
        with open(out_path, 'w') as f:
            print("Output in '%s'" % out_path)
            print("\n".join(m), file=f)

    def cli(self, filters):
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument("-sort_field", type=str)
        for f in filters:
            parser.add_argument("-%s" % f, action="store_true")

        args = parser.parse_args()
        filters_args = {
            f: getattr(args, f)
            for f in filters
        }
        self.explore_results(sort_field=args.sort_field, **filters_args)



def read_rouge(rouge_path):
    """Read ROUGE scores from ROUGE-1.5.5 output (or wrapper)
    Args:
        rouge_path(str): path of ROUGE file
    Returns:
        rouge_scores(dict): all scores,
            {$m: {$s: float}}
            for $m in ['rouge-1', 'rouge-2', 'rouge-l']
            for $m in ['f', 'r', 'p']
    """
    with open(rouge_path, 'r') as f:
        rouge_lines = [_.strip() for _ in f]

    if not len(rouge_lines) == 13:
        raise ValueError("Incorrect ROUGE file (%d != 13 lines) %s" %
              (len(rouge_lines), rouge_path))
    
    rouge_format = {
        "rouge-1": {
            "r": 2,
            "p": 3,
            "f": 4
        },
        "rouge-2": {
            "r": 6,
            "p": 7,
            "f": 8
        },
        "rouge-l": {
            "r": 10,
            "p": 11,
            "f": 12
        }
    }
    def _rouge_value(m, s):
        n = rouge_format[m][s]
        line = rouge_lines[n-1]
        try:
            end = line.split('Average_%s: ' % s.upper())[1]
        except:
            print(line, s, n, line.split('Average_%s: ' % s.upper()))
            raise
        score = end.split()[0]
        return float(score)

    rouge_scores = {
        m: {
            s: _rouge_value(m, s)
            for s in v.keys()
        } for m, v in rouge_format.items()
    }
    return rouge_scores

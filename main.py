from core.signal_extractor import extract_signals
from core.scoring_engine import compute_scores


if __name__ == "__main__":

    conversation = """
    A: You never listen to me.
    B: That’s not true.
    A: You always ignore how I feel.
    B: You’re overreacting again.
    """

    raw_signals = extract_signals(conversation)
    result = compute_scores(raw_signals)

    print(result)


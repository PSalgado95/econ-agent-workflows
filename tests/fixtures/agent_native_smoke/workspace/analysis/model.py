"""Small deterministic calculation used by the review smoke fixture."""

OBSERVATIONS = (1.0, 2.0, 3.0, 4.0)


def sample_mean(values: tuple[float, ...] = OBSERVATIONS) -> float:
    return sum(values) / len(values)


if __name__ == "__main__":
    print(f"{sample_mean():.2f}")

# fact-checker

Verifies the factual claims in any text (a draft, post, transcript, or list of statements) against live, reputable sources. It returns a table that marks each claim Correct, Partially Correct, or Incorrect, with cited references. It is for writers, editors, and researchers who want sourced verdicts instead of recalled answers.

## When to use it
- Before publishing an article, post, or script that contains dates, numbers, or attributions.
- When you want to know whether a claim you read or were sent is true.
- When you need a cited verdict, in the language of the claims, that you can show to others.

## Example request
> Fact-check this: The Eiffel Tower was completed in 1889. Mount Everest is 8,000 meters tall. The Great Wall of China is visible from the Moon with the naked eye. Python was first released in 1991.

## Example output
| Claim | Decision | Evidence & References |
|---|---|---|
| The Eiffel Tower was completed in 1889. | ✅ Correct | Construction was completed on 31 March 1889, and the tower opened to the public on 15 May 1889 [1]. |
| Mount Everest is 8,000 meters tall. | ❌ Incorrect | Nepal and China jointly announced an official height of 8,848.86 m (29,031.7 ft) in 2020, replacing the earlier 8,848 m figure from the 1954 Survey of India [2]. |
| The Great Wall of China is visible from the Moon with the naked eye. | ❌ Incorrect | Astronauts on the Moon, such as Neil Armstrong, reported seeing no man-made structures. Even from low Earth orbit the wall is hard to see and visible only in specific lighting conditions [3]. |
| Python was first released in 1991. | ✅ Correct | Guido van Rossum posted the code to USENET in February 1991, and the earliest release (0.9 series) is dated 1991-02-20 [4][5]. |

**Conclusion**
Two of the four claims are fully verified (the Eiffel Tower and Python dates). The Everest height is off by roughly 850 m, and the Great Wall claim is a long-debunked myth.

**References**
[1] [Eiffel Tower – Wikipedia](https://en.wikipedia.org/wiki/Eiffel_Tower)
[2] [China, Nepal say Everest a bit higher than past measurements – Associated Press via KPRC](https://www.click2houston.com/news/world/2020/12/08/china-nepal-say-everest-a-bit-higher-than-past-measurements/)
[3] [Is China's Great Wall Visible from Space? – Scientific American](https://www.scientificamerican.com/article/is-chinas-great-wall-visible-from-space/)
[4] [General Python FAQ – Python documentation](https://docs.python.org/3/faq/general.html)
[5] [History of Python – Wikipedia](https://en.wikipedia.org/wiki/History_of_Python)

Would you like me to correct the original text to reflect what the evidence shows?

_Last run: 2026-10-12 · Claude Sonnet 5.5_

## Install
```bash
cp -r fact-checker ~/.claude/skills/
```
Full instructions for the agent: [SKILL.md](SKILL.md)

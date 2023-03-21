
from sumy.summarizers.lex_rank import LexRankSummarizer
summarizer_lex = LexRankSummarizer()

# Summarize using sumy LexRank
summary= summarizer_lex("how does thunder work in details", 1)
lex_summary=""
for sentence in summary:
    lex_summary+=str(sentence)
print(lex_summary)
import argparse
import matplotlib.pyplot as plt
from .main import CommentAnalyzer

def entrypoint():
    """Entrypoint for the ytcomment_trends package
    """
    parser = argparse.ArgumentParser(prog='ytcomment_trends', usage='ytcomment_trends -v pR2E2OatMTQ -t "./client_secret.json"', description='ytcomment_trends: YouTube comment trends analysis tool using oseti')
    parser.add_argument('-v', '--video_id', help='YouTube video id', type=str, required=True)
    parser.add_argument('-t', '--token', help='YouTube API token (json) file path', type=str, required=True)
    args = parser.parse_args()

    ca = CommentAnalyzer(args.video_id, args.token)
    ca_comments = ca.get_comments()
    ca_analyzed = ca.get_analyzed_comments(ca_comments)
    ca_summarized = ca.get_summarized_comments(ca_analyzed)

    fig, ax1 = plt.subplots()
    t = list(ca_summarized.index.values)

    color = 'tab:red'
    ax1.set_xlabel('datetime comment posted')
    ax1.set_ylabel('number of comments', color=color)
    ax1.plot(t, list(ca_summarized['snippet.isPublic']), color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()

    oseti_scores = []
    for s, n in zip(list(ca_summarized['oseti_score']), list(ca_summarized['snippet.isPublic'])):
        if n > 0:
            oseti_scores.append(s / n)
        else:
            oseti_scores.append(0)

    color = 'tab:blue'
    ax2.set_ylabel('negative / positive', color=color)
    ax2.plot(t, oseti_scores, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.ylim(-1.2, 1.2)
    plt.title("YouTube Video Comment Trends for " + args.video_id)
    plt.grid(True)

    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    entrypoint()
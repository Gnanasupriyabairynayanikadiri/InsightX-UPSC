def detect_category(title, description):

    text = f"{title} {description}".lower()

    categories = {

        "Polity": [
            "constitution","parliament","court","judgment","election",
            "bill","act","supreme court","president","governor"
        ],

        "Economy": [
            "rbi","inflation","gdp","budget","economy","tax",
            "bank","stock","fiscal","monetary","trade","rupee"
        ],

        "Environment": [
            "climate","forest","biodiversity","pollution",
            "wildlife","ecology","species","cop","carbon"
        ],

        "Science & Technology": [
            "isro","space","satellite","rocket",
            "artificial intelligence","ai","quantum",
            "semiconductor","chip","biotechnology",
            "genome","technology"
        ],

        "International Relations": [
            "iran","usa","united states","china","russia",
            "ukraine","israel","palestine","bangladesh",
            "pakistan","un","united nations","g20",
            "brics","asean","quad","nato",
            "diplomat","embassy","foreign"
        ],

        "Security": [
            "war","missile","military","terrorism",
            "army","navy","air force",
            "border","defence","security"
        ]
    }

    scores = {}

    for category, keywords in categories.items():

        scores[category] = 0

        for keyword in keywords:

            if keyword in text:
                scores[category] += 1

    best = max(scores, key=scores.get)

    if scores[best] == 0:
        return "Misc"

    return best
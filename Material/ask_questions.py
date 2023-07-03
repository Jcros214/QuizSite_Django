import random

questions = [
    {
        "type": "R",
        "reference": "M 5:1",
        "question": "According to Matthew 5:1, where did he go?",
        "answer": "(up) into a mountain"
    },
    {
        "type": "R",
        "reference": "M 5:1",
        "question": "According to Matthew 5:1, when did his disciples come unto him?",
        "answer": "when he was set"
    },
    {
        "type": "R",
        "reference": "M 5:2",
        "question": "According to Matthew 5:2, what 2 things did he do?",
        "answer": "he opened his mouth, and taught them"
    },
    {
        "type": "P",
        "reference": "M 5:2",
        "question": "What in Matthew 5 did Jesus open?",
        "answer": "his mouth"
    },
    {
        "type": "R",
        "reference": "M 5:3",
        "question": "According to Matthew 5:3, who are blessed?",
        "answer": "the poor in spirit"
    },
    {
        "type": "R",
        "reference": "M 5:4",
        "question": "According to Matthew 5:4, who are blessed?",
        "answer": "they that mourn"
    },
    {
        "type": "P",
        "reference": "M 5:4",
        "question": "What shall they that mourn be in Matthew 5?",
        "answer": "they shall be comforted."
    },
    {
        "type": "R",
        "reference": "M 5:5",
        "question": "According to Matthew 5:5, who are blessed?",
        "answer": "the meek"
    },
    {
        "type": "R",
        "reference": "M 5:5",
        "question": "According to Matthew 5:5, what shall the meek inherit?",
        "answer": "the earth"
    },
    {
        "type": "R",
        "reference": "M 5:6",
        "question": "According to Matthew 5:6, who are blessed?",
        "answer": "they which do hunger and thirst after righteousness"
    },
    {
        "type": "P",
        "reference": "M 5:6",
        "question": "Who in Matthew 5 shall be filled?",
        "answer": "they which do hunger and thirst after righteousness"
    },
    {
        "type": "P",
        "reference": "M 5:7",
        "question": "What shall the merciful obtain in Matthew 5?",
        "answer": "mercy"
    },
    {
        "type": "R",
        "reference": "M 5:7",
        "question": "According to Matthew 5:7, who are blessed?",
        "answer": "the merciful"
    },
    {
        "type": "R",
        "reference": "M 5:8",
        "question": "According to Matthew 5:8, who are blessed?",
        "answer": "the pure in heart"
    },
    {
        "type": "P",
        "reference": "M 5:8",
        "question": "What shall the pure in heart do in Matthew 5?",
        "answer": "they shall see God"
    },
    {
        "type": "R",
        "reference": "M 5:9",
        "question": "According to Matthew 5:9, who are blessed?",
        "answer": "the peacemakers"
    },
    {
        "type": "P",
        "reference": "M 5:9",
        "question": "Who in Matthew 5 shall be called the children of God?",
        "answer": "the peacemakers"
    },
    {
        "type": "P",
        "reference": "M 5:10",
        "question": "Whose is the kingdom of heaven in Matthew 5?",
        "answer": "the poor in spirit and  they which are persecuted for righteousness' sake"
    },
    {
        "type": "R",
        "reference": "M 5:10",
        "question": "According to Matthew 5:10, who are blessed?",
        "answer": "they which are persecuted for righteousness' sake"
    },
    {
        "type": "R",
        "reference": "M 5:10",
        "question": "According to Matthew 5:10, whose is the kingdom of heaven?",
        "answer": "they which are persecuted for righteousness' sake"
    },
    {
        "type": "R",
        "reference": "M 5:11",
        "question": "According to Matthew 5:11, when are ye blessed?",
        "answer": "when men shall revile you, and persecute you, and shall say all manner of evil against you falsely, for my sake"
    },
    {
        "type": "P",
        "reference": "M 5:12",
        "question": "Who was persecuted before you in Matthew 5?",
        "answer": "the prophets"
    },
    {
        "type": "R",
        "reference": "M 5:12",
        "question": "According to Matthew 5:12, what is great?",
        "answer": "your reward in heaven"
    },
    {
        "type": "R",
        "reference": "M 5:13",
        "question": "According to Matthew 5:13, what is salt good for if it has lost his savour?",
        "answer": "good for nothing, but to be cast out, and to be trodden under foot of men"
    },
    {
        "type": "P",
        "reference": "M 5:13",
        "question": "Which salt are ye in Matthew 5?",
        "answer": "the salt of the earth"
    },
    {
        "type": "K",
        "reference": "M 5:13",
        "question": "Quote the verse from Matthew 5 which uses the word: salted",
        "answer": "Ye are the salt of the earth: but if the salt have lost his savour, wherewith shall it be salted? it is thenceforth good for nothing, but to be cast out, and to be trodden under foot of men."
    },
    {
        "type": "R",
        "reference": "M 5:14",
        "question": "According to Matthew 5:14, what are ye?",
        "answer": "the light of the world"
    },
    {
        "type": "P",
        "reference": "M 5:14",
        "question": "What is set on a hill in Matthew 5?",
        "answer": "A city"
    },
    {
        "type": "G",
        "reference": "M 5:14",
        "question": "Give the reference: Ye are the light of the world. A city that is set on an hill cannot be hid.",
        "answer": "Matthew 5:14"
    },
    {
        "type": "P",
        "reference": "M 5:15",
        "question": "Where do men put a candle in Matthew 5?",
        "answer": "on a candlestick"
    },
    {
        "type": "R",
        "reference": "M 5:15",
        "question": "According to Matthew 5:15, unto whom does the candle give light?",
        "answer": "all that are in the house"
    },
    {
        "type": "F",
        "reference": "M 5:16",
        "question": "Finish this verse: \"Let your light so shine before men...\"",
        "answer": "that they may see your good works, and glorify your Father which is in heaven"
    },
    {
        "type": "R",
        "reference": "M 5:16",
        "question": "According to Matthew 5:16, whom may men glorify?",
        "answer": "your Father which is in heaven"
    },
    {
        "type": "R",
        "reference": "M 5:16",
        "question": "According to Matthew 5:16, what may men see?",
        "answer": "your good works"
    },
    {
        "type": "R",
        "reference": "M 5:17",
        "question": "According to Matthew 5:17, what am I come to do?",
        "answer": "to fulfil (the law and the prophets)"
    },
    {
        "type": "R",
        "reference": "M 5:17",
        "question": "According to Matthew 5:17, what think not?",
        "answer": "that I (Jesus) am come to destroy the law, or the prophets"
    },
    {
        "type": "P",
        "reference": "M 5:18",
        "question": "From what shall one jot or one tittle in no wise pass, till all be fulfilled, in Matthew 5?",
        "answer": "from the law"
    },
    {
        "type": "P",
        "reference": "M 5:19",
        "question": "Who shall be called great in the kingdom of heaven in Matthew 5?",
        "answer": "whosoever shall do and teach them (these least commandments)"
    },
    {
        "type": "R",
        "reference": "M 5:19",
        "question": "According to Matthew 5:19, what shall he be called that shall break one of these least commandments?",
        "answer": "the least in the kingdom of heaven"
    },
    {
        "type": "R",
        "reference": "M 5:20",
        "question": "According to Matthew 5:20, except what, ye shall in no case enter into the kingdom of heaven?",
        "answer": "except your righteousness shall exceed the righteousness of the scribes and Pharisees"
    },
    {
        "type": "Q",
        "reference": "M 5:20",
        "question": "Quote this verse: Matthew 5:20.",
        "answer": "For I say unto you, That except your righteousness shall exceed the righteousness of the scribes and Pharisees, ye shall in no case enter into the kingdom of heaven."
    },
    {
        "type": "R",
        "reference": "M 5:21",
        "question": "According to Matthew 5:21, by whom was it said, Thou shalt not kill?",
        "answer": "by them of old time"
    },
    {
        "type": "R",
        "reference": "M 5:21",
        "question": "According to Matthew 5:21, who shall be in danger of judgment?",
        "answer": "whosoever shall kill"
    },
    {
        "type": "P",
        "reference": "M 5:22",
        "question": "Whosoever is angry with his brother without a cause shall be in danger of what in Matthew 5?",
        "answer": "the judgment"
    },
    {
        "type": "P",
        "reference": "M 5:22",
        "question": "Whosoever shall say, Thou fool, shall be in danger of what in Matthew 5?",
        "answer": "hell fire"
    },
    {
        "type": "R",
        "reference": "M 5:23",
        "question": "According to Matthew 5:23, what rememberest thou at the altar?",
        "answer": "that thy brother hath ought against thee"
    },
    {
        "type": "P",
        "reference": "M 5:24",
        "question": "When be reconciled to thy brother in Matthew 5?",
        "answer": "first"
    },
    {
        "type": "R",
        "reference": "M 5:24",
        "question": "According to Matthew 5:24, what leave there before the altar?",
        "answer": "thy gift"
    },
    {
        "type": "P",
        "reference": "M 5:25",
        "question": "When agree with thine adversary in Matthew 5?",
        "answer": "quickly (whiles thou art in the way with him)"
    },
    {
        "type": "R",
        "reference": "M 5:25",
        "question": "According to Matthew 5:25, where may you be cast?",
        "answer": "into prison"
    },
    {
        "type": "P",
        "reference": "M 5:26",
        "question": "What must be paid before you can come out of prison in Matthew 5?",
        "answer": "the uttermost farthing"
    },
    {
        "type": "R",
        "reference": "M 5:27",
        "question": "According to Matthew 5:27, what shalt thou not do?",
        "answer": "Thou shalt not commit adultery"
    },
    {
        "type": "P",
        "reference": "M 5:28",
        "question": "Who hath committed adultery with a woman already in his heart in Matthew 5?",
        "answer": "whosoever looketh on a woman to lust after her"
    },
    {
        "type": "R",
        "reference": "M 5:29",
        "question": "According to Matthew 5:29, what pluck out?",
        "answer": "thy right eye if it offend thee"
    },
    {
        "type": "P",
        "reference": "M 5:29",
        "question": "What is profitable for thee in Matthew 5?",
        "answer": "that one of thy members should perish, and not that thy whole body should be cast into hell"
    },
    {
        "type": "R",
        "reference": "M 5:30",
        "question": "According to Matthew 5:30, what cut off?",
        "answer": "thy right hand if it offend thee"
    },
    {
        "type": "R",
        "reference": "M 5:31",
        "question": "According to Matthew 5:31, let whom give her a writing of divorcement?",
        "answer": "(him) Whosoever shall put away his wife"
    },
    {
        "type": "P",
        "reference": "M 5:32",
        "question": "Who committeth adultery in Matthew 5?",
        "answer": "whosoever shall marry her that is divorced"
    },
    {
        "type": "R",
        "reference": "M 5:32",
        "question": "According to Matthew 5:32, who causeth his wife to commit adultery?",
        "answer": "whosoever shall put away his wife, saving for the cause of fornication"
    },
    {
        "type": "P",
        "reference": "M 5:33",
        "question": "What perform unto the Lord in Matthew 5?",
        "answer": "thine oaths"
    },
    {
        "type": "R",
        "reference": "M 5:33",
        "question": "According to Matthew 5:33, by whom hath it been said, Thou shalt not forswear thyself, but shalt perform unto the Lord thine oaths?",
        "answer": "by them of old time"
    },
    {
        "type": "R",
        "reference": "M 5:34",
        "question": "According to Matthew 5:34, why swear not by heaven?",
        "answer": "for it is God's throne"
    },
    {
        "type": "R",
        "reference": "M 5:35",
        "question": "According to Matthew 5:35, what is Jerusalem?",
        "answer": "the city of the great King"
    },
    {
        "type": "P",
        "reference": "M 5:35",
        "question": "What in Matthew 5 is his footstool?",
        "answer": "the earth"
    },
    {
        "type": "P",
        "reference": "M 5:36",
        "question": "By what 4 swear not in Matthew 5?",
        "answer": "heaven,  the earth,  Jerusalem,  thy head"
    },
    {
        "type": "P",
        "reference": "M 5:36",
        "question": "What canst thou not make black or white in Matthew 5?",
        "answer": "one hair"
    },
    {
        "type": "R",
        "reference": "M 5:36",
        "question": "According to Matthew 5:36, why swear not by thy head?",
        "answer": "because thou canst not make one hair white or black"
    },
    {
        "type": "P",
        "reference": "M 5:37",
        "question": "What let your communication be in Matthew 5?",
        "answer": "Yea, yea; Nay, nay"
    },
    {
        "type": "R",
        "reference": "M 5:37",
        "question": "According to Matthew 5:37, what cometh of evil?",
        "answer": "whatsoever is more than these (Yea, yea; Nay, nay)"
    },
    {
        "type": "P",
        "reference": "M 5:38",
        "question": "What for a tooth in Matthew 5?",
        "answer": "a tooth"
    },
    {
        "type": "R",
        "reference": "M 5:38",
        "question": "According to Matthew 5:38, what for an eye?",
        "answer": "An eye"
    },
    {
        "type": "P",
        "reference": "M 5:39",
        "question": "What resist not in Matthew 5?",
        "answer": "evil"
    },
    {
        "type": "R",
        "reference": "M 5:39",
        "question": "According to Matthew 5:39, what turn to whosoever shall smite thee on thy right cheek?",
        "answer": "the other (cheek) also"
    },
    {
        "type": "P",
        "reference": "M 5:40",
        "question": "Let whom have thy cloak also in Matthew 5?",
        "answer": "if any man will sue thee at the law and take away thy coat"
    },
    {
        "type": "R",
        "reference": "M 5:41",
        "question": "According to Matthew 5:41, go with whom twain?",
        "answer": "whosoever shall compel thee to go a mile"
    },
    {
        "type": "F",
        "reference": "M 5:41",
        "question": "Finish this verse: \"And whosoever shall compel thee...\"",
        "answer": "to go a mile, go with him twain"
    },
    {
        "type": "R",
        "reference": "M 5:42",
        "question": "According to Matthew 5:42, from whom turn not away?",
        "answer": "from him that would borrow of thee"
    },
    {
        "type": "R",
        "reference": "M 5:42",
        "question": "According to Matthew 5:42, to whom give?",
        "answer": "to him that asketh thee"
    },
    {
        "type": "R",
        "reference": "M 5:43",
        "question": "According to Matthew 5:43, whom hate?",
        "answer": "thine enemy"
    },
    {
        "type": "R",
        "reference": "M 5:43",
        "question": "According to Matthew 5:43, what hath been said?",
        "answer": "Thou shalt love thy neighbour, and hate thine enemy"
    },
    {
        "type": "R",
        "reference": "M 5:43",
        "question": "According to Matthew 5:43, love whom?",
        "answer": "thy neighbour"
    },
    {
        "type": "R",
        "reference": "M 5:44",
        "question": "According to Matthew 5:44, for whom pray?",
        "answer": "for them which despitefully use you, and persecute you"
    },
    {
        "type": "R",
        "reference": "M 5:44",
        "question": "According to Matthew 5:44, love whom?",
        "answer": "your enemies"
    },
    {
        "type": "R",
        "reference": "M 5:44",
        "question": "According to Matthew 5:44, to whom do good?",
        "answer": "to them that hate you"
    },
    {
        "type": "P",
        "reference": "M 5:44",
        "question": "Bless whom in Matthew 5?",
        "answer": "them that curse you"
    },
    {
        "type": "P",
        "reference": "M 5:45",
        "question": "Who sendeth rain on the just and on the unjust in Matthew 5?",
        "answer": "your Father (which is in heaven)"
    },
    {
        "type": "R",
        "reference": "M 5:45",
        "question": "According to Matthew 5:45, on whom does he make his sun to rise?",
        "answer": "on the evil and on the good"
    },
    {
        "type": "R",
        "reference": "M 5:46",
        "question": "According to Matthew 5:46, who do the same?",
        "answer": "the publicans"
    },
    {
        "type": "R",
        "reference": "M 5:47",
        "question": "According to Matthew 5:47, what do publicans do?",
        "answer": "(so) salute their brethren"
    },
    {
        "type": "R",
        "reference": "M 5:48",
        "question": "According to Matthew 5:48, what is your Father which is in heaven?",
        "answer": "perfect"
    },
    {
        "type": "R",
        "reference": "M 5:48",
        "question": "According to Matthew 5:48, what be ye?",
        "answer": "perfect"
    },
    {
        "type": "R",
        "reference": "M 6:1",
        "question": "According to Matthew 6:1, who is in heaven?",
        "answer": "your Father"
    },
    {
        "type": "R",
        "reference": "M 6:1",
        "question": "According to Matthew 6:1, where do not your alms?",
        "answer": "before men"
    },
    {
        "type": "P",
        "reference": "M 6:2",
        "question": "What in Matthew 6 sound not before thee?",
        "answer": "a trumpet"
    },
    {
        "type": "R",
        "reference": "M 6:2",
        "question": "According to Matthew 6:2, what do the hypocrites have?",
        "answer": "their reward"
    },
    {
        "type": "R",
        "reference": "M 6:3",
        "question": "According to Matthew 6:3, when let not thy left hand know what thy right hand doeth?",
        "answer": "when thou doest alms"
    },
    {
        "type": "R",
        "reference": "M 6:4",
        "question": "According to Matthew 6:4, how shall thy Father reward thee?",
        "answer": "openly"
    },
    {
        "type": "R",
        "reference": "M 6:4",
        "question": "According to Matthew 6:4, what may be in secret?",
        "answer": "thine alms"
    },
    {
        "type": "R",
        "reference": "M 6:5",
        "question": "According to Matthew 6:5, as whom shalt thou not be?",
        "answer": "as the hypocrites"
    },
    {
        "type": "R",
        "reference": "M 6:5",
        "question": "According to Matthew 6:5, where do the hypocrites love to pray?",
        "answer": "(standing) in the synagogues and in the corners of the streets"
    },
    {
        "type": "K",
        "reference": "M 6:5",
        "question": "Quote the verse from Matthew 6 which uses the word: corners",
        "answer": "And when thou prayest, thou shalt not be as the hypocrites are: for they love to pray standing in the synagogues and in the corners of the streets, that they may be seen of men. Verily I say unto you, They have their reward."
    },
    {
        "type": "R",
        "reference": "M 6:6",
        "question": "According to Matthew 6:6, how does thy Father see?",
        "answer": "in secret"
    },
    {
        "type": "P",
        "reference": "M 6:6",
        "question": "When enter into thy closet in Matthew 6?",
        "answer": "when thou prayest"
    },
    {
        "type": "R",
        "reference": "M 6:7",
        "question": "According to Matthew 6:7, what do the heathen think?",
        "answer": "that they shall be heard for their much speaking"
    },
    {
        "type": "P",
        "reference": "M 6:7",
        "question": "Who use vain repetitions in Matthew 6?",
        "answer": "the heathen"
    },
    {
        "type": "R",
        "reference": "M 6:8",
        "question": "According to Matthew 6:8, when does your Father know what things ye have need of?",
        "answer": "before ye ask him"
    },
    {
        "type": "R",
        "reference": "M 6:8",
        "question": "According to Matthew 6:8, why be not like the heathen?",
        "answer": "for your Father knoweth what things ye have need of, before ye ask him"
    },
    {
        "type": "P",
        "reference": "M 6:9",
        "question": "What be hallowed in Matthew 6?",
        "answer": "thy name (our Father's name)"
    },
    {
        "type": "R",
        "reference": "M 6:10",
        "question": "According to Matthew 6:10, where is thy will done?",
        "answer": "in heaven"
    },
    {
        "type": "R",
        "reference": "M 6:10",
        "question": "According to Matthew 6:10, what come?",
        "answer": "Thy kingdom"
    },
    {
        "type": "R",
        "reference": "M 6:11",
        "question": "According to Matthew 6:11, when give us our daily bread?",
        "answer": "this day"
    },
    {
        "type": "R",
        "reference": "M 6:11",
        "question": "According to Matthew 6:11, what give us?",
        "answer": "our daily bread"
    },
    {
        "type": "R",
        "reference": "M 6:12",
        "question": "According to Matthew 6:12, what forgive us?",
        "answer": "our debts"
    },
    {
        "type": "R",
        "reference": "M 6:12",
        "question": "According to Matthew 6:12, how does God forgive us our debts?",
        "answer": "as we forgive our debtors"
    },
    {
        "type": "R",
        "reference": "M 6:13",
        "question": "According to Matthew 6:13, from what deliver us?",
        "answer": "evil"
    },
    {
        "type": "R",
        "reference": "M 6:13",
        "question": "According to Matthew 6:13, what 3 are thine?",
        "answer": "the kingdom, and the power, and the glory"
    },
    {
        "type": "R",
        "reference": "M 6:14",
        "question": "According to Matthew 6:14, when will your heavenly Father forgive you?",
        "answer": "if ye forgive men their trespasses"
    },
    {
        "type": "R",
        "reference": "M 6:14",
        "question": "According to Matthew 6:14, what do you forgive men?",
        "answer": "their trespasses"
    },
    {
        "type": "R",
        "reference": "M 6:15",
        "question": "According to Matthew 6:15, when will your Father not forgive your trespasses?",
        "answer": "if ye forgive not men their trespasses"
    },
    {
        "type": "P",
        "reference": "M 6:16",
        "question": "What is sad in Matthew 6?",
        "answer": "(the hypocrites') countenance"
    },
    {
        "type": "P",
        "reference": "M 6:16",
        "question": "Why do hypocrites disfigure their faces in Matthew 6?",
        "answer": "that they may appear unto men to fast"
    },
    {
        "type": "P",
        "reference": "M 6:17",
        "question": "When anoint thy head in Matthew 6?",
        "answer": "when thou fastest"
    },
    {
        "type": "R",
        "reference": "M 6:17",
        "question": "According to Matthew 6:17, what 2 things do when thou fastest?",
        "answer": "anoint thine head, and wash thy face"
    },
    {
        "type": "R",
        "reference": "M 6:18",
        "question": "According to Matthew 6:18, how appear unto men?",
        "answer": "not to fast"
    },
    {
        "type": "R",
        "reference": "M 6:18",
        "question": "According to Matthew 6:18, what shall thy Father do?",
        "answer": "shall reward thee openly"
    },
    {
        "type": "R",
        "reference": "M 6:19",
        "question": "According to Matthew 6:19, where lay not up treasures?",
        "answer": "upon earth"
    },
    {
        "type": "P",
        "reference": "M 6:19",
        "question": "Where do moth and rust corrupt in Matthew 6?",
        "answer": "upon earth"
    },
    {
        "type": "F",
        "reference": "M 6:19",
        "question": "Finish this verse: \"Lay not up for yourselves treasures upon earth... \"",
        "answer": "where moth and rust doth corrupt, and where thieves break through and steal"
    },
    {
        "type": "P",
        "reference": "M 6:19",
        "question": "Who break through and steal in Matthew 6?",
        "answer": "thieves"
    },
    {
        "type": "R",
        "reference": "M 6:20",
        "question": "According to Matthew 6:20, what lay up for yourselves?",
        "answer": "treasures in heaven"
    },
    {
        "type": "P",
        "reference": "M 6:20",
        "question": "Where do thieves not break through nor steal in Matthew 6?",
        "answer": "in heaven"
    },
    {
        "type": "G",
        "reference": "M 6:20",
        "question": "Give the reference: But lay up for yourselves treasures in heaven, where neither moth nor rust doth corrupt, and where thieves do not break through nor steal:",
        "answer": "Matthew 6:20"
    },
    {
        "type": "Q",
        "reference": "M 6:21",
        "question": "Quote this verse: Matthew 6:21.",
        "answer": "For where your treasure is, there will your heart be also."
    },
    {
        "type": "R",
        "reference": "M 6:21",
        "question": "According to Matthew 6:21, where will your heart be?",
        "answer": "(there) where your treasure is"
    },
    {
        "type": "P",
        "reference": "M 6:21",
        "question": "What will be where your treasure is in Matthew 6?",
        "answer": "your heart"
    },
    {
        "type": "R",
        "reference": "M 6:22",
        "question": "According to Matthew 6:22, what is the eye?",
        "answer": "The light of the body"
    },
    {
        "type": "R",
        "reference": "M 6:22",
        "question": "According to Matthew 6:22, what shall be full of light?",
        "answer": "thy whole body"
    },
    {
        "type": "R",
        "reference": "M 6:23",
        "question": "According to Matthew 6:23, when shall thy whole body be full of darkness?",
        "answer": "if thine eye be evil"
    },
    {
        "type": "P",
        "reference": "M 6:24",
        "question": "Whom can you not serve with mammon in Matthew 6?",
        "answer": "God"
    },
    {
        "type": "P",
        "reference": "M 6:24",
        "question": "Who in Matthew 6 can serve 2 masters?",
        "answer": "No man"
    },
    {
        "type": "G",
        "reference": "M 6:24",
        "question": "Give the reference: No man can serve two masters: for either he will hate the one, and love the other; or else he will hold to the one, and despise the other. Ye cannot serve God and mammon.",
        "answer": "Matthew 6:24"
    },
    {
        "type": "R",
        "reference": "M 6:24",
        "question": "According to Matthew 6:24, why can no man serve 2 masters?",
        "answer": "for either he will hate the one, and love the other; or else he will hold to the one, and despise the other"
    },
    {
        "type": "R",
        "reference": "M 6:25",
        "question": "According to Matthew 6:25, what is more than raiment?",
        "answer": "the body"
    },
    {
        "type": "R",
        "reference": "M 6:25",
        "question": "According to Matthew 6:25, for what 5 take no thought?",
        "answer": "for your life, what ye shall eat, or what ye shall drink; nor yet for your body, what ye shall put on"
    },
    {
        "type": "P",
        "reference": "M 6:26",
        "question": "Who feedeth the fowls of the air in Matthew 6?",
        "answer": "your heavenly Father"
    },
    {
        "type": "P",
        "reference": "M 6:26",
        "question": "Who do not gather into barns in Matthew 6?",
        "answer": "the fowls of the air"
    },
    {
        "type": "R",
        "reference": "M 6:26",
        "question": "According to Matthew 6:26, what 3 do fowls not do?",
        "answer": "they sow not, neither do they reap, nor gather into barns"
    },
    {
        "type": "P",
        "reference": "M 6:27",
        "question": "Can you add what unto your stature in Matthew 6?",
        "answer": "one cubit"
    },
    {
        "type": "P",
        "reference": "M 6:28",
        "question": "What consider in Matthew 6?",
        "answer": "the lilies of the field"
    },
    {
        "type": "P",
        "reference": "M 6:28",
        "question": "What toil not in Matthew 6?",
        "answer": "the lilies of the field"
    },
    {
        "type": "R",
        "reference": "M 6:28",
        "question": "According to Matthew 6:28, what 2 things do lilies not do?",
        "answer": "they toil not, neither do they spin"
    },
    {
        "type": "P",
        "reference": "M 6:29",
        "question": "Who was not arrayed like one of the lilies of the field in Matthew 6?",
        "answer": "(even) Solomon (in all his glory)"
    },
    {
        "type": "P",
        "reference": "M 6:30",
        "question": "When in Matthew 6 is the grass cast into the oven?",
        "answer": "to morrow"
    },
    {
        "type": "P",
        "reference": "M 6:30",
        "question": "What does God clothe in Matthew 6?",
        "answer": "the grass of the field"
    },
    {
        "type": "R",
        "reference": "M 6:31",
        "question": "According to Matthew 6:31, what take?",
        "answer": "no thought"
    },
    {
        "type": "R",
        "reference": "M 6:32",
        "question": "According to Matthew 6:32, who seek after all these things?",
        "answer": "the Gentiles"
    },
    {
        "type": "R",
        "reference": "M 6:32",
        "question": "According to Matthew 6:32, what does your heavenly Father know?",
        "answer": "that ye have need of all these things"
    },
    {
        "type": "F",
        "reference": "M 6:33",
        "question": "Finish this verse: \"But seek ye first the kingdom of God... \"",
        "answer": "and his righteousness; and all these things shall be added unto you"
    },
    {
        "type": "P",
        "reference": "M 6:33",
        "question": "What shall be added unto you in Matthew 6?",
        "answer": "all these things"
    },
    {
        "type": "R",
        "reference": "M 6:33",
        "question": "According to Matthew 6:33, when seek the kingdom of God and his righteousness?",
        "answer": "first"
    },
    {
        "type": "P",
        "reference": "M 6:33",
        "question": "What seek first in Matthew 6?",
        "answer": "the kingdom of God, and his righteousness"
    },
    {
        "type": "P",
        "reference": "M 6:34",
        "question": "What is sufficient unto the day in Matthew 6?",
        "answer": "the evil thereof"
    },
    {
        "type": "R",
        "reference": "M 6:34",
        "question": "According to Matthew 6:34, what shall take thought for the things of itself?",
        "answer": "the morrow"
    },
    {
        "type": "R",
        "reference": "M 6:34",
        "question": "According to Matthew 6:34, what take for the morrow?",
        "answer": "no thought"
    },
    {
        "type": "P",
        "reference": "M 7:1",
        "question": "Why in Matthew 7 judge not?",
        "answer": "that ye be not judged"
    },
    {
        "type": "P",
        "reference": "M 7:2",
        "question": "How shall it be measured to you again in Matthew 7?",
        "answer": "with what measure ye mete"
    },
    {
        "type": "P",
        "reference": "M 7:2",
        "question": "How shall ye be judged in Matthew 7?",
        "answer": "with what judgment ye judge"
    },
    {
        "type": "P",
        "reference": "M 7:3",
        "question": "What is in thy brother's eye in Matthew 7?",
        "answer": "the mote"
    },
    {
        "type": "R",
        "reference": "M 7:3",
        "question": "According to Matthew 7:3, what beholdest thou?",
        "answer": "the mote that is in thy brother's eye"
    },
    {
        "type": "R",
        "reference": "M 7:3",
        "question": "According to Matthew 7:3, where is the beam?",
        "answer": "in thine own eye"
    },
    {
        "type": "R",
        "reference": "M 7:4",
        "question": "According to Matthew 7:4, what is in thine own eye?",
        "answer": "a beam"
    },
    {
        "type": "P",
        "reference": "M 7:4",
        "question": "What let me pull out in Matthew 7?",
        "answer": "the mote out of thine eye (thy brother's eye)"
    },
    {
        "type": "R",
        "reference": "M 7:5",
        "question": "According to Matthew 7:5, how shalt thou then see to cast out the mote out of thy brother's eye?",
        "answer": "clearly"
    },
    {
        "type": "R",
        "reference": "M 7:5",
        "question": "According to Matthew 7:5, when cast the beam out of thine own eye?",
        "answer": "first"
    },
    {
        "type": "P",
        "reference": "M 7:6",
        "question": "Who may trample pearls under their feet in Matthew 7?",
        "answer": "swine"
    },
    {
        "type": "P",
        "reference": "M 7:6",
        "question": "Where cast not your pearls in Matthew 7?",
        "answer": "before swine"
    },
    {
        "type": "R",
        "reference": "M 7:6",
        "question": "According to Matthew 7:6, what give not unto the dogs?",
        "answer": "that which is holy"
    },
    {
        "type": "G",
        "reference": "M 7:7",
        "question": "Give the reference: Ask, and it shall be given you; seek, and ye shall find; knock, and it shall be opened unto you:",
        "answer": "Matthew 7:7"
    },
    {
        "type": "R",
        "reference": "M 7:7",
        "question": "According to Matthew 7:7, what 3 do?",
        "answer": "Ask, seek, and knock"
    },
    {
        "type": "R",
        "reference": "M 7:8",
        "question": "According to Matthew 7:8, to whom shall it be opened?",
        "answer": "to him that knocketh"
    },
    {
        "type": "F",
        "reference": "M 7:8",
        "question": "Finish this verse: \"For every one that asketh receiveth ; and he that... \"",
        "answer": "seeketh findeth; and to him that knocketh it shall be opened"
    },
    {
        "type": "R",
        "reference": "M 7:9",
        "question": "According to Matthew 7:9, what may his son ask?",
        "answer": "bread"
    },
    {
        "type": "R",
        "reference": "M 7:10",
        "question": "According to Matthew 7:10, what may he ask?",
        "answer": "a fish"
    },
    {
        "type": "R",
        "reference": "M 7:11",
        "question": "According to Matthew 7:11, what do ye now?",
        "answer": "how to give good gifts unto your children"
    },
    {
        "type": "R",
        "reference": "M 7:11",
        "question": "According to Matthew 7:11, to whom shall your father give good things?",
        "answer": "to them that ask him"
    },
    {
        "type": "R",
        "reference": "M 7:12",
        "question": "According to Matthew 7:12, what is this?",
        "answer": "the law and the prophets"
    },
    {
        "type": "R",
        "reference": "M 7:12",
        "question": "According to Matthew 7:12, what do ye even so to men?",
        "answer": "all things whatsoever ye would that men should do to you"
    },
    {
        "type": "K",
        "reference": "M 7:13",
        "question": "Quote the verse from Matthew 7 which uses the word: destruction",
        "answer": "Enter ye in at the strait gate: for wide is the gate, and broad is the way, that leadeth to destruction, and many there be which go in thereat:"
    },
    {
        "type": "P",
        "reference": "M 7:13",
        "question": "What is wide in Matthew 7?",
        "answer": "the gate (that leadeth to destruction)"
    },
    {
        "type": "R",
        "reference": "M 7:13",
        "question": "According to Matthew 7:13, who go in there at?",
        "answer": "many"
    },
    {
        "type": "P",
        "reference": "M 7:14",
        "question": "What is strait in Matthew 7?",
        "answer": "the gate (which leadeth unto life)"
    },
    {
        "type": "P",
        "reference": "M 7:14",
        "question": "What is narrow in Matthew 7?",
        "answer": "the way which leadeth unto life"
    },
    {
        "type": "R",
        "reference": "M 7:14",
        "question": "According to Matthew 7:14, who find it?",
        "answer": "few"
    },
    {
        "type": "K",
        "reference": "M 7:14",
        "question": "Quote the verse from Matthew 7 which uses the word: narrow",
        "answer": "Because strait is the gate, and narrow is the way, which leadeth unto life, and few there be that find it."
    },
    {
        "type": "R",
        "reference": "M 7:15",
        "question": "According to Matthew 7:15, how do the false prophets come to you?",
        "answer": "in sheep's clothing"
    },
    {
        "type": "R",
        "reference": "M 7:15",
        "question": "According to Matthew 7:15, beware of whom?",
        "answer": "false prophets"
    },
    {
        "type": "P",
        "reference": "M 7:15",
        "question": "Inwardly, what are the false prophets in Matthew 7?",
        "answer": "ravening wolves"
    },
    {
        "type": "R",
        "reference": "M 7:16",
        "question": "According to Matthew 7:16, by what shall you know them?",
        "answer": "by their fruits"
    },
    {
        "type": "R",
        "reference": "M 7:17",
        "question": "According to Matthew 7:17, what bringeth forth evil fruit?",
        "answer": "a corrupt tree"
    },
    {
        "type": "R",
        "reference": "M 7:17",
        "question": "According to Matthew 7:17, what does every good tree bring forth?",
        "answer": "good fruit"
    },
    {
        "type": "R",
        "reference": "M 7:18",
        "question": "According to Matthew 7:18, what can a good tree not bring forth?",
        "answer": "evil fruit"
    },
    {
        "type": "R",
        "reference": "M 7:18",
        "question": "According to Matthew 7:18, what cannot bring forth good fruit?",
        "answer": "a corrupt tree"
    },
    {
        "type": "Q",
        "reference": "M 7:20",
        "question": "Quote this verse: Matthew 7:20.",
        "answer": "Wherefore by their fruits ye shall know them."
    },
    {
        "type": "R",
        "reference": "M 7:20",
        "question": "According to Matthew 7:20, how shall ye know them?",
        "answer": "by their fruits"
    },
    {
        "type": "R",
        "reference": "M 7:21",
        "question": "According to Matthew 7:21, who shall enter into the kingdom of heaven?",
        "answer": "he that doeth the will of my Father which is in heaven"
    },
    {
        "type": "R",
        "reference": "M 7:21",
        "question": "According to Matthew 7:21, what does one say?",
        "answer": "Lord, Lord"
    },
    {
        "type": "R",
        "reference": "M 7:22",
        "question": "According to Matthew 7:22, what 3 things will many say they have done in thy name?",
        "answer": "prophesied in thy name, in thy name have cast out devils, and in thy name done many wonderful works"
    },
    {
        "type": "R",
        "reference": "M 7:22",
        "question": "According to Matthew 7:22, when will many say, Lord, Lord?",
        "answer": "in that day"
    },
    {
        "type": "P",
        "reference": "M 7:23",
        "question": "What will I profess unto them in Matthew 7?",
        "answer": "I never knew you (depart from me, ye that work iniquity)"
    },
    {
        "type": "R",
        "reference": "M 7:23",
        "question": "According to Matthew 7:23, who depart from me?",
        "answer": "ye that work iniquity"
    },
    {
        "type": "P",
        "reference": "M 7:24",
        "question": "Where did the wise man build his house in Matthew 7?",
        "answer": "upon a rock"
    },
    {
        "type": "R",
        "reference": "M 7:24",
        "question": "According to Matthew 7:24, whom will I liken unto a wise man?",
        "answer": "whosoever heareth these sayings of mine, and doeth them"
    },
    {
        "type": "Q",
        "reference": "M 7:25",
        "question": "Quote this verse: Matthew 7:25.",
        "answer": "And the rain descended, and the floods came, and the winds blew, and beat upon that house; and it fell not: for it was founded upon a rock."
    },
    {
        "type": "R",
        "reference": "M 7:25",
        "question": "According to Matthew 7:25, why did the house not fall?",
        "answer": "for it was founded upon a rock"
    },
    {
        "type": "R",
        "reference": "M 7:25",
        "question": "According to Matthew 7:25, what descended?",
        "answer": "the rain"
    },
    {
        "type": "P",
        "reference": "M 7:26",
        "question": "Who built his house upon the sand in Matthew 7?",
        "answer": "a foolish man"
    },
    {
        "type": "R",
        "reference": "M 7:26",
        "question": "According to Matthew 7:26, who shall be likened unto a foolish man?",
        "answer": "every one that heareth these sayings of mine, and doeth them not"
    },
    {
        "type": "R",
        "reference": "M 7:27",
        "question": "According to Matthew 7:27, what came?",
        "answer": "the floods"
    },
    {
        "type": "P",
        "reference": "M 7:27",
        "question": "What in Matthew 7 was great?",
        "answer": "the fall of (it) the foolish man's house"
    },
    {
        "type": "R",
        "reference": "M 7:28",
        "question": "According to Matthew 7:28, who were astonished at his doctrine?",
        "answer": "the people"
    },
    {
        "type": "R",
        "reference": "M 7:29",
        "question": "According to Matthew 7:29, not as whom did Jesus teach them?",
        "answer": "the scribes"
    },
    {
        "type": "R",
        "reference": "M 7:29",
        "question": "According to Matthew 7:29, how did Jesus teach them?",
        "answer": "as one having authority (and not as the scribes)"
    }
]

random.shuffle(questions)

while len(questions) > 0:
    question = questions.pop(0)
    if question['reference'].startswith('M 5:'):
        print(question['question'])
        print(question['answer'])
        print(question['reference'])
        print(question['type'] + '\n\n\n\n\n')
        input()

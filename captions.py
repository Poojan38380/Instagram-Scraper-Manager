import random


def get_random_caption():
    captions_options = [
        "No problem! Here's the information about the Mercedes CLR GTR:\n\nThe Mercedes CLR GTR is a remarkable racing car celebrated for its outstanding performance and sleek design. Powder by a potent 6.0-liter V12 engine, it delivers over 600 horsepower.📷 Acceleration from 0 to 100km/h takes approximately 3.7 seconds, with a remarkable top speed surpassing 320km/h. \n\n📷 Incorporation advanced aerodynamic features and cutting-edge stability technologies, the ClR GTR ensures exceptional stability and control, particularly during high-speed maneuvers. 📷 Originally priced around $1.5 million, the Mercedes CLR GTR is considered one of the most exclusive and prestigious racing cars ever produced. \n\n📷 It's limited production run of just five units adds to its rarity, making it highly sought after by racing enthusiasts and collectors worldwide. 📷"
    ]
    return random.choice(captions_options)

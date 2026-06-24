characters=[{
  "name": "Jonas",
  "secret":"killed the host",
  "deflects_about":"thinks he got away with it,later guilty conscience and confesses",
  
}, {
  "name": "Rachel",
  "secret":"sham marriage,loves a commoner",
  "deflects_about":"doesn't want the family pressure to be exposed",
  "personality": "shy, introverted, tends to avoid confrontation and prefers to keep to herself. She's deeply affected by the secrets and lies surrounding her, which creates a sense of isolation and anxiety."
},{
  "name":"Nick",
  "secret":"was bullied by the host,best-friend and love-hate girl",
  "deflects_about":"too proud/hurt to admit it",
  "personality": "broody, closed off, speaks in short clipped sentences, doesn't explain himself, gets cold and sharp when Daisy is mentioned, the kind of person who shows anger not sadness, would never openly discuss his feelings.When university is mentioned his jaw tightens, he gets quieter, more controlled — he won't say what happened but his reaction makes it obvious something did. He might say something like 'some people don't change' or 'let's just say not everyone deserves what they have' before shutting down"
  },{
    "name":"Daisy",
    "secret":"was a bully, loves the man she bullied",
    "deflects_about":"shame and guilt",
    "personality": "warm, charming, effortlessly social — the kind of person who makes everyone feel like they're her favorite. But there's something performative about it, like she's working very hard to be likeable. Gets subtly uncomfortable when Nick is mentioned, changes the subject smoothly. Her warmth has a brittle edge if you push past it. Would never bring up the past unprompted — she's spent years pretending it didn't happen.",
    "personality_confronted": "the charm completely drops, she gets quiet and small, speaks in fragments, can't maintain eye contact, the guilt she's been suppressing for years surfaces all at once. She doesn't deny it when directly confronted with proof — she just breaks."
  },{
    "name":"Camilla",
    "secret":"affair with host",
    "deflects_about":"protecting herself and her marriage",
    "personality": "calm, composed, polite, measured, speaks in a soft voice, doesn't raise her voice or get flustered. She has a quiet confidence and is very self-assured. She doesn't get defensive or angry when confronted but breaks down when the affair is revealed, showing a side of her that is vulnerable and emotional. She has a strong sense of self-preservation and will do whatever it takes to protect herself and her marriage."
  },{
    "name":"William",
    "secret":"knows about the affair,is gay,had feelings for the host",
    "deflects_about":"hiding his sexuality and heartbreak",
    "personality": "reserved, polite, and formal, speaks in a measured tone, doesn't raise his voice or get flustered. He has a quiet confidence and is very self-assured. He doesn't get defensive or angry when confronted but breaks down once he admits to player whatever he heard on terrace revealing he is gay and had feelings for host from some time."
  },{
    "name":"Marcus",
    "secret":"was a bully, killed by best-friend and loves th couple-wife"
  }
]
unlock_rules = {
    "Nick": None,  # Nick is unlocked from start, player is suspicious of him
    "Rachel": None,
    "Daisy": {"clue_found": "bullying_records"},
    "Camilla": {
        "interrogated": "Nick", "min_times": 2,
        "and": {"interrogated": "Daisy", "min_times": 1}
    },
    "Jonas": {"interrogated": "Camilla", "min_times": 1},
    "William": {"interrogated": "Jonas", "min_times": 1},
}
location_rules = {
    "host_study": {"interrogated": "Nick"},
    "terrace": {"clue_found": "bullying_records"},
    "library": {"interrogated": "Daisy"},
    "guest_room_Jonas": {"interrogated": "Camilla"},
    "guest_room_Marcus": None,      # open from start
    "guest_room_Nick": None,  # open from start
    "guest_room_Rachel": None,  # open from start
    "guest_room_Camilla": {"interrogated": "Daisy"},  # open from start
    "garden": None,
    "ballroom": None,
    "guest_room_William": {"interrogated": "Jonas"},
}
clues = {
    "bullying_records": {
        "found_at": "host_study",
        "unlocks_locations": ["terrace"],
        "unlocks_characters": ["Daisy"],
        "description": "Disturbing accounts of systematic bullying at the host's university, enough to make anyone angry."
    },
    "university_yearbook": {
        "found_at": "library",
        "unlocks_locations": [],
        "unlocks_characters": [],
        "description": "A yearbook showing the host, bestfriend and love-hate girl were all at the same university — a breadcrumb, not a clue."
    }
}

bestfriend_arc = {
    "calm": "appears composed and cooperative during interrogations annd tries blaming it on suicide",
    "cracking": "shows signs of stress and guilt and remembers his moments with the host",
    "breaking": "confesses to the murder, revealing the motive and details of the crime"
}


     

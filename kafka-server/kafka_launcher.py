import kafka_producer as kp

topics = ["tickers", "user_signup", "user_login"]

for i in topics:
    topic_name = topics[i]
    topics[i] = kp.Data_source(topics[i])
    print(f"Topic {topic_name} has been launched")






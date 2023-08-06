# kafka_admin_service

Kafka admin service class, provides basic management functions such as USER creation, USER deletion, USER listing all and USER password changing, TOPIC creation, TOPIC deletion, TOPIC listing all, and ACL creation, ACL deletion and ACL listing all.

## Install

```
pip install kafka-admin-service
```

## KafkaAdminService methods

- add_acl
- change_password
- create_topic
- create_topic_and_topic_user
- create_user
- delete_acl
- delete_all_topics
- delete_all_users
- delete_topic
- delete_topic_user_acls
- delete_user
- get_acls
- get_topics
- get_user_scrams
- get_users
- update_user
- validate_user_password

## Releases

### v0.1.1 2021/12/14

- First Release.

### v0.1.3 2021/12/14

- Fix kafka commands' path check.
- Add execute time log.

### v0.1.6 2021/12/17

- Add get_user_scrams method.
- Add validate_user_password method.

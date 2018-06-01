# flavor-house
2018S KAIST DB Project #2
## API Instructions
1. 회원가입
1. 로그인
1. 유저 정보
1. 즐겨찾기 등록
1. 즐겨찾기 취소
1. 즐겨찾기 목록
1. 식당 정보
1. 키워드로 식당 검색
1. 태그로 식당 검색
## Server Info
```
Protocol: HTTP
Base URI: 13.125.127.34
Port: 3000
```
---
## 회원가입
- URL - /user
- Method - POST
- Request
```
Form data {
    id: < str >,
    password: < str >,
    name: < str >
}
```
- Response
```
JSON {
    result: < str | 성공시 'success' >
}
```
---
## 로그인
- URL - /user/login
- Method - POST
- Request
```
Form data {
    user_id: < int >,
    password: < str >
}
```
- Response
```
JSON {
    result: < str | 성공시 'success' >,
    data: {
        user_id: < int >,
        name: < str >
    }
}
```
---
## 유저 정보
- URL - /user
- Method - GET
- Request
```
Query string {
    user_id: < int >
}
```
- Response
```
JSON {
    result: < str | 성공시 'success' >,
    data: {
        user_id: < int >,
        name: < str >,
        favorite_list: [{
            store_id: < int >,
            name: < str >,
            category: < str >,
            score: < float >
        }]
    }
}
```
---
## 즐겨찾기 등록
- URL - /user/favorite
- Method - POST
- Request
```
Form data {
    user_id: < int >,
    store_id: < int >
}
```
- Response
```
JSON {
    result: < str | 성공시 'success' >
}
```
---
## 즐겨찾기 취소
- URL - /user/favorite
- Method - DELETE
- Request
```
Query string {
    user_id: < int >,
    store_id: < int >
}
```
- Response
```
JSON {
    result: < str | 성공시 'success' >
}
```
---
## 즐겨찾기 목록
- URL - /user/favorite
- Method - GET
- Request
```
Query string {
    user_id: < int >
}
```
- Response
```
JSON {
    result: < str | 성공시 'success' >,
    data: [{
        store_id: < int >,
        name: < str >,
        category: < str >,
        score: < float >
    }]
}
```
---
## 식당 정보
- URL - /store
- Method - GET
- Request
```
Query string {
    store_id: < int >
}
```
- Response
```
JSON {
    result: < str | 성공시 'success' >,
    data: {
        store_id: < int >,
        name: < str >,
        category: < str >,
        description: < str >,
        score: < float >,
        review_list: [{
            content: < str >,
            likes: < int >,
            date: < date >
        }],
        tag_list: [ < str > ]
    }
}
```
---
## 키워드로 식당 검색
- URL - /store/list/keyword
- Method - GET
- Request
```
Query string {
    keyword: < str >
}
```
- Response
```
JSON {
    result: < str | 성공시 'success' >,
    data: [{
        store_id: < int >,
        name: < str >,
        category: < str >,
        description: < str >,
        score: < float >,
        review_list: [{
            content: < str >,
            likes: < int >,
            date: < date >
        }],
        tag_list: [ < str > ]
    }]
}
```
---
## 태그로 식당 검색
- URL - /store/list/tag
- Method - GET
- Request
```
Query string {
    tag: < str >
}
```
- Response
```
JSON {
    result: < str | 성공시 'success' >,
    data: [{
        store_id: < int >,
        name: < str >,
        category: < str >,
        description: < str >,
        score: < float >,
        review_list: [{
            content: < str >,
            likes: < int >,
            date: < date >
        }],
        tag_list: [ < str > ]
    }]
}
```
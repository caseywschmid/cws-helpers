# How to upload a course

To upload a full course takes a few steps. This guide outlines how to upload the structure of the course, how to upload each individual item’s content (article, question, video) and finally how to view it in flashcards.

Base URL: https://api.alpha1edtech.com

## 1. Course Structure Upload

### 1.1 Create the Course

Endpoint: POST /courses

Request Body:

```json
{
  "status": "active",
  "title": "Course Title",
  "schoolYear": 2024,
  "courseCode": "COURSE_CODE",
  "grades": 9,
  "subjects": "Subject Name",
  "subjectCodes": "SUBJECT_CODE"
}
```

Response: The API will return a course ID. Store this for future use.

### 1.2 Create Modules(Grades/Units)

For each module in the course:
Endpoint: POST /modules

Request Body:

```json
{
  "name": "Module Name",
  "unlock_at": "2024-04-22T03:09:38.515Z",
  "state": "active"
}
```

### 1.3 Set Module Relationships

To create prerequisites between modules:
Endpoint: POST /modules/associations

Request Body:

```json
{
  "originModuleId": "previous_module_id",
  "destinationModuleId": "current_module_id",
  "relationship": "prerequisite"
}
```

### 1.4 Add Items to Modules

For each item in a module:
Endpoint: POST /modules/{module_id}/items

Request Body:

```json
{
  "name": "Item Name",
  "state": "active",
  "lti_url": "https://example.com/item",
  "xp": "Integer for amount of XP awarded on completion",
  "contentType": "article" // or "video", "exercise", "quiz"
}
```

Response: The API will return an item ID. Store this for each item.

### 1.5 Set Item Relationships

To create prerequisites between items within a module:
Endpoint: POST /modules/{module_id}/items/associations

Request Body:

```json
{
  "originItemId": "previous_item_id",
  "destinationItemId": "current_item_id",
  "relationship": "prerequisfunite",
  "moduleId": "module_id"
}
```

### 1.6 Set Starting Item for Module

Endpoint: PATCH /modules/{module_id}

```json
Request Body:
{
  "startingItemId": "first_item_id_in_module"
}
```

### 1.7 Set Default Module for Course

Endpoint: PATCH /courses/{course_id}

Request Body:

```json
{
  "defaultModuleId": "first_module_id"
}
```

## 2. Content Upload

Note: All content is uploaded into “questionBank”. This represents a content bank, which could be videos, questions or articles.

### 2.1 Articles

Endpoint: PUT /modules/{moduleId}/items/{item_id}
Request Body:

```json
{
  "metadata": "Full article text, markdown or HTML content"
}
```

### 2.2 Videos

Endpoint: POST /modules/{moduleId}/items/{item_id}/questionBank
Request Body:

```json
{
  "questionBank": [
    {
      "material": "a video url such as https://www.youtube.com/watch?v=NiT7PBiEooo",
      "responses": []
    }
  ]
}
```

### 2.3 Exercises/Questions

Endpoint: POST /modules/{moduleId}/items/{item_id}/questionBank
Request Body:

```json
{
  "questionBank": [
    {
      "material": "Question text",
      "referenceText": "Reference text for the question",
      "responses": [
        {
          "label": "Answer 1 content",
          "isCorrect": true,
          "explanation": "This is right because"
        },
        {
          "label": "Answer 2 content",
          "isCorrect": false,
          "explanation": "This is wrong because"
        }
      ],
      "difficulty": 1 // One of 1, 2 or 3 (easy, medium, hard)
    }
  ]
}
```

# PowerPath API Helper

This package provides tools for working with the PowerPath API. It includes models, API clients, utility functions, and usage examples.

## Installation

This helper is included in the `cws-helpers` package. Install it using:

```bash
# Install the latest version
pip install git+https://github.com/caseywschmid/cws-helpers.git

# Install a specific version using a tag
pip install git+https://github.com/caseywschmid/cws-helpers.git@v0.1.0
```

For requirements.txt:
```
# Always get the latest version
git+https://github.com/caseywschmid/cws-helpers.git

# Or pin to a specific version tag
git+https://github.com/caseywschmid/cws-helpers.git@v0.1.0
```

## Authentication

**Note:** As of now, no authentication is required to use the PowerPath API.

## Implementation Status

The following table shows the implementation status of API functions for each endpoint:

| Category      | Implemented | Total | Progress |
|---------------|-------------|-------|----------|
| Courses       | 5           | 5     | 100%     |
| Users         | 7           | 7     | 100%     |
| Goals         | 5           | 5     | 100%     |
| XP            | 2           | 2     | 100%     |
| Results       | 5           | 5     | 100%     |
| Progress      | 4           | 4     | 100%     |
| Modules       | 14          | 14    | 100%     |
| Questions     | 3           | 3     | 100%     |
| Responses     | 3           | 3     | 100%     |
| Question Banks| 4           | 4     | 100%     |
| SQL           | 1           | 1     | 100%     |
| **Total**     | **53**      | **53**| **100%**|

**Note:** All available API endpoints have been implemented.

## Quick Start

```python
from cws_helpers.powerpath_helper import PowerPathClient, get_all_courses

# Initialize the client
# The base URL "https://api.alpha1edtech.com" is set by default
client = PowerPathClient()

# Get all courses
courses = get_all_courses(client)
print(f"Found {len(courses)} courses")
```

## Basic Usage

```python
from cws_helpers.powerpath_helper import PowerPathClient

# Initialize the client
# The base URL "https://api.alpha1edtech.com" is set by default
client = PowerPathClient()

# Use the client to interact with the API
courses = client.get("/courses")
print(f"Found {len(courses)} courses")
```

## Using API Functions

The PowerPath API helper provides high-level functions for interacting with the API. Here's how to use them:

```python
from cws_helpers.powerpath_helper import (
    PowerPathClient,
    get_all_courses,
    get_course,
    PowerPathCourse,
    create_course
)

# Initialize the client
# The base URL "https://api.alpha1edtech.com" is set by default
client = PowerPathClient()

# Get all courses
courses = get_all_courses(client)
print(f"Found {len(courses)} courses")

# Get a specific course
course_id = "123"
course = get_course(client, course_id)
print(f"Course name: {course.title}")

# Create a new course
new_course_data = {
    "title": "Introduction to Python",
    "courseCode": "PY101"
}
new_course = PowerPathCourse(**new_course_data)
created_course = create_course(client, new_course.to_create_dict())
print(f"Created course with ID: {created_course.id}")
```

## Usage Examples

### Working with Users

```python
from cws_helpers.powerpath_helper import (
    PowerPathClient,
    PowerPathUser,
    get_all_users,
    search_users,
    get_user,
    create_user,
    update_user,
    delete_user
)

# Initialize the client
client = PowerPathClient()

# Get all users
users = get_all_users(client)
print(f"Found {len(users)} users")

# Search for users by email
search_results = search_users(client, {"email": "student@example.com"})
print(f"Found {len(search_results)} users matching the search criteria")

# Get a specific user
user_id = "123"
user = get_user(client, user_id)
print(f"User name: {user.given_name} {user.family_name}")

# Create a new user
new_user_data = {
    "email": "new.student@example.com",
    "givenName": "Jane",
    "familyName": "Doe"
}
created_user = create_user(client, new_user_data)
print(f"Created user with ID: {created_user.id}")

# Update a user
update_data = {
    "status": "active",
    "preferredFirstName": "J"
}
updated_user = update_user(client, user_id, update_data)
print(f"Updated user: {updated_user.preferred_first_name}")

# Delete a user
result = delete_user(client, user_id)
print("User deleted successfully" if result.get("success") else "Failed to delete user")
```

### Working with Courses and Modules

```python
from cws_helpers.powerpath_helper import (
    PowerPathClient,
    PowerPathCourse,
    PowerPathModule,
    PowerPathItem,
    get_all_courses,
    get_course,
    create_course,
    get_module,
    create_module,
    get_module_items,
    create_module_item
)

# Initialize the client
client = PowerPathClient()

# Create a new course
course_data = {
    "title": "Data Science Fundamentals",
    "courseCode": "DS101"
}
course = create_course(client, course_data)
print(f"Created course: {course.title} (ID: {course.id})")

# Create a module in the course
module_data = {
    "name": "Introduction to Python",
    "state": "active"
}
module = create_module(client, module_data)
print(f"Created module: {module.name} (ID: {module.id})")

# Create an item in the module
item_data = {
    "name": "Python Basics Quiz",
    "contentType": "quiz",
    "xp": 100
}
item = create_module_item(client, module.id, item_data)
print(f"Created item: {item.name} (ID: {item.id})")

# Get all items in a module
items = get_module_items(client, module.id)
print(f"Module has {len(items)} items")
```

### Working with User Progress

```python
from cws_helpers.powerpath_helper import (
    PowerPathClient,
    get_user_course_progress,
    get_user_module_progress,
    get_user_item_progress,
    get_user_results,
    create_user_result,
    get_user_xp,
    create_user_xp
)

# Initialize the client
client = PowerPathClient()

# Get a user's progress in a course
user_id = "123"
course_id = "456"
progress = get_user_course_progress(client, user_id, course_id)
print(f"User has progress in {len(progress)} modules")

# Get a user's progress in a specific module
module_id = "789"
module_progress = get_user_module_progress(client, user_id, module_id)
print(f"Module progress: {module_progress[0].name}")

# Get a user's progress on a specific item
item_id = "101"
item_progress = get_user_item_progress(client, user_id, item_id)
print(f"Item progress: {item_progress}")

# Create a result for a user
result_data = {
    "type": "assessment",
    "value": 85.5,
    "achievedLevel": "proficient"
}
result = create_user_result(client, user_id, result_data)
print(f"Created result with ID: {result.id}")

# Get a user's XP
xp_records = get_user_xp(client, user_id)
print(f"User has {len(xp_records)} XP records")

# Create XP for a user
xp_data = {
    "amount": 100,
    "courseId": course_id,
    "subject": "Mathematics"
}
xp = create_user_xp(client, user_id, xp_data)
print(f"Created XP record with ID: {xp.id}")
```

### Working with Goals

```python
from cws_helpers.powerpath_helper import (
    PowerPathClient,
    get_user_goals,
    create_user_goal,
    update_user_goal,
    delete_user_goal,
    get_course_goals
)

# Initialize the client
client = PowerPathClient()

# Get a user's goals
user_id = "123"
goals = get_user_goals(client, user_id)
print(f"User has {len(goals)} goals")

# Create a goal for a user
goal_data = {
    "description": "Complete 10 math exercises",
    "xp": 500,
    "courseId": 789,
    "cutoffDate": "2023-12-31T23:59:59Z"
}
goal = create_user_goal(client, user_id, goal_data)
print(f"Created goal with ID: {goal.id}")

# Update a goal
goal_id = "456"
update_data = {
    "description": "Complete 20 math exercises",
    "xp": 1000
}
updated_goal = update_user_goal(client, user_id, goal_id, update_data)
print(f"Updated goal: {updated_goal.description}")

# Delete a goal
result = delete_user_goal(client, user_id, goal_id)
print("Goal deleted successfully" if result.get("success") else "Failed to delete goal")

# Get all goals for a course
course_id = "789"
users_with_goals = get_course_goals(client, course_id)
print(f"Course has {len(users_with_goals)} users with goals")
```

### Advanced: Using SQL Queries

```python
from cws_helpers.powerpath_helper import (
    PowerPathClient,
    execute_sql_query
)

# Initialize the client
client = PowerPathClient()

# Execute a custom SQL query
sql_query = """
SELECT u.id, u.email, u.givenName, u.familyName, COUNT(r.id) as result_count
FROM users u
LEFT JOIN results r ON u.id = r.userId
GROUP BY u.id
ORDER BY result_count DESC
LIMIT 10
"""
results = execute_sql_query(client, sql_query)
print(f"Query returned {len(results)} rows")
for row in results:
    print(f"User: {row['givenName']} {row['familyName']}, Results: {row['result_count']}")
```

### Working with Models

The PowerPath API helper provides Pydantic models for all PowerPath resources. These models can be used to validate data and convert between Python objects and API data.

```python
from cws_helpers.powerpath_helper import (
    PowerPathUser,
    PowerPathCourse,
    PowerPathModule,
    PowerPathItem,
    PowerPathGoal,
    PowerPathXP,
    PowerPathResult
)

# Create a user model
user = PowerPathUser(
    email="student@example.com",
    givenName="John",
    familyName="Doe",
    username="johndoe",
    status="active"
)

# Convert to a dictionary for API operations
user_dict = user.to_create_dict()
print(user_dict)

# Create a course model
course = PowerPathCourse(
    title="Introduction to Python",
    courseCode="PY101"
)

# Convert to a dictionary for API operations
course_dict = course.to_create_dict()
print(course_dict)
```

### Using a Different Base URL

By default, the client uses "https://api.alpha1edtech.com" as the base URL. If you need to use a different URL (for example, for testing or development), you can specify it when creating the client:

```python
# Initialize the client with a custom base URL
client = PowerPathClient(base_url="https://dev-api.example.com")
```

## Error Handling

The PowerPath API helper provides custom exceptions for handling errors:

```python
from cws_helpers.powerpath_helper import (
    PowerPathClient,
    PowerPathClientError,
    PowerPathRequestError,
    PowerPathAuthenticationError,
    PowerPathNotFoundError,
    PowerPathServerError,
    PowerPathRateLimitError
)

client = PowerPathClient()

try:
    # Try to get a non-existent course
    course = client.get("/courses/999999")
except PowerPathNotFoundError:
    print("Course not found")
except PowerPathAuthenticationError:
    print("Authentication failed")
except PowerPathServerError:
    print("Server error")
except PowerPathRateLimitError:
    print("Rate limit exceeded")
except PowerPathRequestError as e:
    print(f"Request error: {e}")
except PowerPathClientError as e:
    print(f"Client error: {e}")
```

## Examples

The `examples` directory contains sample scripts demonstrating how to use the PowerPath API helper. See the [examples README](./examples/README.md) for more information.

## API Reference

### Implemented API Functions

- **Courses**

  - `get_all_courses(client)` - GET /courses
  - `get_course(client, course_id)` - GET /courses/:courseId
  - `create_course(client, course_data)` - POST /courses
  - `update_course(client, course_id, course_data)` - PATCH /courses/:courseId
  - `delete_course(client, course_id)` - DELETE /courses/:courseId

- **Users**

  - `get_all_users(client)` - GET /users
  - `search_users(client, search_params)` - GET /users with query parameters
  - `list_users(client, term, limit=None, offset=None)` - GET /users/list
  - `get_user(client, user_id)` - GET /users/:studentId
  - `create_user(client, user_data)` - POST /users
  - `update_user(client, user_id, user_data)` - PATCH /users/:studentId
  - `delete_user(client, user_id)` - DELETE /users/:studentId

- **Modules**

  - `get_all_modules(client)` - GET /modules
  - `get_module(client, module_id)` - GET /modules/:moduleId
  - `create_module(client, module_data)` - POST /modules
  - `update_module(client, module_id, module_data)` - PATCH /modules/:moduleId
  - `delete_module(client, module_id)` - DELETE /modules/:moduleId
  - `get_module_items(client, module_id)` - GET /modules/:moduleId/items
  - `get_module_item(client, module_id, item_id)` - GET /modules/:moduleId/items/:itemId
  - `create_module_item(client, module_id, item_data)` - POST /modules/:moduleId/items
  - `update_module_items(client, module_id, items_data)` - PUT /modules/:moduleId/items
  - `create_module_association(client, association_data)` - POST /modules/associations
  - `update_module_association(client, association_data)` - PATCH /modules/associations
  - `delete_module_association(client, origin_module_id, destination_module_id)` - DELETE /modules/associations/:originModuleId/:destinationModuleId
  - `get_item_associations(client, module_id, item_id)` - GET /modules/:moduleId/items/:itemId/associations
  - `create_item_association(client, module_id, association_data)` - POST /modules/:moduleId/items/associations
  - `associate_item_with_module(client, module_id, item_id)` - POST /modules/:moduleId/items/:itemId/associations
  - `update_item_associations(client, module_id, item_id, association_data)` - PATCH /modules/:moduleId/items/:itemId/associations
  - `delete_item_associations(client, module_id, item_id)` - DELETE /modules/:moduleId/items/:itemId/associations
  - `delete_item_association(client, module_id, origin_item_id, destination_item_id)` - DELETE /modules/:moduleId/items/:originItemId/associations/:destinationItemId
  - `get_question_bank(client, module_id, item_id)` - GET /modules/:moduleId/items/:itemId/questionBank
  - `create_question_bank_item(client, module_id, item_id, question_data)` - POST /modules/:moduleId/items/questionBank
  - `delete_question_bank_item(client, module_id, item_id, question_id)` - DELETE /modules/:moduleId/items/:itemId/questionBank/:ccitemId
  - `delete_object_bank(client, module_id, item_id)` - DELETE /modules/:moduleId/items/:itemId/objectBank

- **Questions**

  - `get_question(client, question_id)` - GET /modules/ccItem/:ccItemId
  - `create_question(client, question_data)` - POST /modules/ccItem
  - `update_question(client, question_id, question_data)` - PUT /modules/ccItem/:ccItemId

- **Responses**
  - `create_question_response(client, question_id, response_data)` - POST /modules/ccItem/:ccItemId/responses
  - `update_response(client, response_id, response_data)` - PUT /modules/responses/:responseId
  - `delete_response(client, response_id)` - DELETE /modules/responses/:responseId

- **Module Associations**
  - `get_module_associations(client, module_id)` - Custom SQL query to get all associations for a module

- **SQL**
  - `execute_sql_query(client, sql_query)` - POST /sql

- **Results**
  - `get_user_results(client, user_id, item_id=None, cc_item_id=None, start_date=None, end_date=None)` - GET /users/:studentId/results with optional filters
  - `get_user_result(client, user_id, result_id)` - GET /users/:studentId/results/:resultId
  - `create_user_result(client, user_id, result_data)` - POST /users/:studentId/results
  - `update_user_result(client, user_id, result_id, result_data)` - PATCH /users/:studentId/results/:resultId
  - `delete_user_result(client, user_id, result_id)` - DELETE /users/:studentId/results/:resultId

- **XP**
  - `get_user_xp(client, user_id, course_id=None, course_code=None, subject=None, item_id=None)` - GET /users/:studentId/xp with optional filters
  - `create_user_xp(client, user_id, xp_data)` - POST /users/:studentId/xp

- **Goals**
  - `get_user_goals(client, user_id)` - GET /users/:studentId/goals
  - `create_user_goal(client, user_id, goal_data)` - POST /users/:studentId/goals
  - `update_user_goal(client, user_id, goal_id, goal_data)` - PATCH /users/:studentId/goals/:goalId
  - `delete_user_goal(client, user_id, goal_id)` - DELETE /users/:studentId/goals/:goalId
  - `get_course_goals(client, course_id)` - GET /courses/:courseId/goals

- **Progress**
  - `get_user_course_progress(client, user_id, course_id)` - GET /users/:studentId/courses/:courseId
  - `get_user_course_progress_v2(client, user_id, course_id)` - GET /users/:studentId/courses/:courseId/v2
  - `get_user_module_progress(client, user_id, module_id)` - GET /users/:studentId/modules/:moduleId
  - `get_user_item_progress(client, user_id, item_id)` - GET /users/:studentId/items/:itemId

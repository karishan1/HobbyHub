🎨 Hobbies Web App
A Django + Vue web application that allows users to create accounts, manage their profiles, track hobbies, find similar users, and send friend requests.

🚀 Features
User Authentication: Signup, login, and logout using Django's authentication system with a custom user model.
Profile Management: Users can update their name, email, date of birth, password, and hobbies.
Hobbies Database: Users can select existing hobbies or add new ones, which become available to all users.
Find Similar Users: View users with the most hobbies in common, sorted in descending order, with pagination.
Filtering by Age: Users can filter results by age range via AJAX requests.
Friend Requests: Users can send & accept friend requests via Vue + fetch API.
🛠️ Tech Stack
Backend: Django, Django REST Framework (DRF)
Frontend: Vue 3 (TypeScript), Fetch API
Database: PostgreSQL / SQLite
Authentication: Django's built-in authentication
Testing: Selenium-based end-to-end (E2E) tests
🔬 Automated Testing
The project includes tests for:
✅ Account creation (signup)
✅ Login
✅ Editing profile data
✅ Viewing users & filtering by age
✅ Sending a friend request
✅ Accepting friend requests

🌍 Deployment
The app is deployed on EECS OpenShift.
Preloaded with:
✔️ 20 test users
✔️ 10 hobbies


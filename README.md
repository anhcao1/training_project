# 🛠️ Task Management System - New Employee Training Program

## 📌 Objectives

This project serves as a training exercise for new employees to:

- Master backend development techniques with Django and Django REST Framework.
- Get familiar with the company's project structure and software development workflow.
- Quickly integrate into the team by simulating real project experience.

## 🚀 Key Features

### 1. User Management and Role-Based Access Control
- **Registration**: New users are registered with the default role `Staff`. Admins can create users with any role (`Admin`, `Manager`, `Staff`).
- **Authentication**: Login via JWT (SimpleJWT) to receive access and refresh tokens.
- **User Info Endpoint**: `/api/users/me/` returns the profile of the authenticated user.
- **Role-Based Permissions**:
  - **Admin**: Full access to all system features.
  - **Manager**: Can view, edit, delete, and assign tasks to others.
  - **Staff**: Can only access tasks they created or were assigned.

### 2. Task Management Module
- Task Model includes:
  - `title`, `description`, `status`, `priority`, `owner`, `assignee`, `created_at`, `due_date`.
- Task Status options: `Pending`, `In Progress`, `Completed`, `Cancelled`.
- CRUD Operations:
  - **Staff**: Can create tasks and assign them to themselves. Can only read/update their own tasks.
  - **Manager/Admin**: Full CRUD access to all tasks.
  - **Delete**: Only allowed by Manager or Admin.
- Filtering and Searching:
  - Filter tasks by `status` and `priority`.
  - Search tasks by `title`.

### 3. Background Tasks with Celery
- **Email Notifications**:
  - When a new task is created.
  - When a task's status changes.
- **Deadline Reminders** (Daily at 8:00 AM):
  - Automatically scan for tasks due within the next 24 hours and notify assignees via email.

### 4. Task Statistics API
- Endpoint `/api/stats/`:
  - Returns task count grouped by status for the last 7 days.
  - Accessible only by **Admin** and **Manager** roles.

### 5. Full Dockerization
- Services:
  - `web`, `db`, `redis`, `worker`, `beat`
- Run everything with a single command:
  ```bash
  docker-compose up --build

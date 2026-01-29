# End-to-End Test Flow: Todo Full-Stack Web Application

## Test Flow Overview
This document describes the end-to-end user flows that should be tested to ensure the application functions correctly.

## Flow 1: New User Registration and Task Management

### Step 1: User Registration
1. Navigate to `/auth/register`
2. Fill in registration form:
   - Email: `testuser@example.com`
   - Name: `Test User`
   - Password: `SecurePassword123`
   - Confirm Password: `SecurePassword123`
3. Submit form
4. Verify:
   - User is redirected to dashboard
   - Success message is displayed
   - User information is displayed in header

### Step 2: Create First Task
1. On dashboard, locate "Create New Task" section
2. Fill in task form:
   - Title: `First Task` (2-100 chars)
   - Description: `This is my first task` (optional, up to 1000 chars)
3. Submit form
4. Verify:
   - Task appears in "Your Tasks" list
   - Task shows as "Pending" status
   - Task details are correct

### Step 3: Update Task
1. In the task list, find the created task
2. Click the edit icon
3. Update task details:
   - Change title to `Updated First Task`
   - Update description if needed
4. Submit update
5. Verify:
   - Task details are updated in the list
   - UI reflects changes immediately

### Step 4: Complete Task
1. In the task list, find the task
2. Check the completion checkbox
3. Verify:
   - Task status changes to "Completed"
   - Visual indication (strikethrough) appears
   - Status badge updates to green

### Step 5: Delete Task
1. In the task list, find the task
2. Click the delete icon
3. Confirm deletion in the prompt
4. Verify:
   - Task is removed from the list
   - Success confirmation appears

## Flow 2: Login and Task Management

### Step 1: User Login
1. Navigate to `/auth/login`
2. Fill in login form:
   - Email: `testuser@example.com`
   - Password: `SecurePassword123`
3. Submit form
4. Verify:
   - User is redirected to dashboard
   - User information is displayed in header

### Step 2: Task Operations
1. Perform all operations from Flow 1, Steps 2-5
2. Verify all functionality works as expected

## Flow 3: Authentication Protection

### Step 1: Access Protected Route
1. Navigate directly to `/dashboard` without being logged in
2. Verify:
   - User is redirected to `/auth/login`
   - No access to protected content

### Step 2: Token Expiration
1. Login and stay on dashboard for 1 hour (simulated)
2. Perform an action (e.g., create task)
3. Verify:
   - User is redirected to login
   - Error message about session expiration (if applicable)

## Flow 4: User Isolation

### Step 1: Data Isolation
1. Login as User A
2. Create several tasks
3. Logout
4. Login as User B
5. Verify:
   - User B does not see User A's tasks
   - User B only sees their own tasks (if any)

## Flow 5: Error Handling

### Step 1: Invalid Registration
1. Navigate to `/auth/register`
2. Submit form with invalid data:
   - Email: `invalid-email`
   - Name: `T` (too short)
   - Password: `123` (too short)
3. Verify:
   - Appropriate error messages appear
   - Form remains populated
   - No account is created

### Step 2: Invalid Login
1. Navigate to `/auth/login`
2. Submit form with incorrect credentials
3. Verify:
   - Error message appears
   - Form remains populated
   - No access granted

### Step 3: Invalid Task Creation
1. On dashboard, try to create a task with:
   - Title: `A` (too short)
   - Or empty title
2. Verify:
   - Appropriate error messages appear
   - Form remains populated
   - No task is created

## Performance Requirements
- All API requests should return within 2 seconds under normal load
- Page loads should complete within 3 seconds
- Form submissions should provide immediate feedback

## Expected Success Criteria
- All user flows complete without errors
- Data persists correctly between sessions
- Security measures prevent unauthorized access
- User experience is smooth and intuitive
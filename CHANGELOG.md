## 0.6.0 (2024-08-31)

### Feat

- **backend**: rabbitmq reconnection
- **backend**: confirm code expired at check
- **api**: standard response and validation
- **backend**: get single position and update single position

## 0.5.0 (2024-08-30)

### Feat

- **frontend**: update forms
- **backend**: create positions
- **backend**: refactor database
- **backend**: position price range
- **backend**: add position models
- **backend**: auth and role required middlewares
- **backend**: run application with live reload
- **backend**: )confirm account
- **backend**: confirm code table
- **backend**: create rabbitmq connection and events
- **backend**: register candidate
- **db**: remove models import from alembic env.py and add company logo field
- **db**: fix alembic change detection
- **db**: models and migrations
- **backend**: setup alembic
- **backend**: update application structure and db
- **ui**: setup ngrx store
- **ui**: add password confirm custom validator fn
- **ui**: text-input
- **public**: working with templates
- **public**: mocking ui
- **public**: better modules tree
- **public**: base structure public application
- **ui**: add route resolver for apply position page

### Fix

- **frontend**: rename public to client project
- **ui**: register as a company component
- **db**: incorrect "default" usage on created_at fields

### Refactor

- **backend**: remove nested async with, move code selection in reporsitory method, etc
- **backend**: designing registration backend
- **backend**: saving progress
- **backend**: refactoring backend to use new database models
- **backend**: structure
- general refactoring

## 0.4.0 (2024-05-19)

### Feat

- **ui**: select skills simple select component

### Fix

- **ui**: back to bootstrap

## 0.3.0 (2024-05-18)

### Feat

- **ui**: update ui
- **ui**: check out primeng ui kit

### Fix

- **ui**: add footer menu

## 0.2.0 (2024-05-18)

### Feat

- **ui**: position list, applying form, results form
- **ui**: basic ui and services

## 0.1.0 (2024-05-18)

### Feat

- **backend**: dockerize backend
- **backend**: apply form and get results by submission secret
- **backend**: apply form candidate, list of candidates and positions
- **backend**: create positions with skills
- **backend**: position get/create endpoints ( not tested )
- **backend**: positions repository
- **backend**: add skills api endpoints
- **backend**: add example timeout middleware
- **backend**: add users list
- **backend**: validate user creation from db prospective
- **backend**: user auth stuff
- **backend**: create admin
- **backend**: auth
- **backend**: structure backend application
- **db**: create models
- **api**: add service template

### Refactor

- **backend**: use getpass to promt admin password
- **backend**: move to orm 02
- **backend**: move to orm tables 01

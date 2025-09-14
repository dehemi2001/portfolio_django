# Django Dynamic Portfolio

A fully dynamic personal portfolio website built with Django. All content, including user information, skills, and projects, can be managed easily through the Django admin panel.

# Live Demo

*[Add your live demo link here]*

---

## Running the Project Locally 🚀

Follow these steps to get your own version of the portfolio running on your local machine.

### Prerequisites

* Python 3.8+
* Git

### 1. Clone the Repository

First, clone the repository to your local machine and navigate into the directory:
```bash
git clone https://github.com/dehemi2001/django_portfolio.git
cd django_portfolio
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

On Windows:
```bash
source .venv/Scripts/activate
```
On macOS/Linux:
```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```
Or, if `requirements.txt` is missing:
```bash
pip install django
```

### 5. Set Up the Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser Account

This account lets you log in to the Django admin panel and add your portfolio details.
```bash
python manage.py createsuperuser
```
Follow the prompts to set username, email, and password.

### 7. Run the Development Server

```bash
python manage.py runserver
```
The project will be available at: **http://localhost:8000**

---

## Add Your Portfolio Details

1. Open your browser and go to **http://localhost:8000/admin**
2. Log in using the superuser credentials you created.
3. Add your details:
    - **User**: Add your personal information (name, avatar, resume, etc.).
    - **Skills**: Add your skills, percentage, and color.
    - **Projects**: Add your projects, descriptions, GitHub/live links, and order.
    - **Contact**: (Optional) View messages sent via the contact form.

4. Refresh the homepage (**http://localhost:8000**) to see your portfolio live!

---

## Customization

- To change styles, edit files in [`static/css/`](static/css/).
- To update images, add them to [`static/images/`](static/images/).
- To modify templates, edit [`Base/templates/home.html`](Base/templates/home.html).

---

## Troubleshooting

- If you see an empty homepage, make sure you have added at least one User entry in the admin panel.
- For media uploads (avatars, resumes), ensure the [`media/`](media/) directory exists and is writable.

---

Enjoy your dynamic portfolio!
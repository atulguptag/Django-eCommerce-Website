# FootFusion: A Django eCommerce Website

<div align="center">

[![GitHub issues](https://img.shields.io/github/issues/atulguptag/Django-eCommerce-Website?color=pink&logo=github)](https://github.com/atulguptag/Django-eCommerce-Website/issues)
![GitHub forks](https://img.shields.io/github/forks/atulguptag/Django-eCommerce-Website?logo=git)
![GitHub Repo stars](https://img.shields.io/github/stars/atulguptag/Django-eCommerce-Website)
[![Contributors](https://img.shields.io/github/contributors/atulguptag/Django-eCommerce-Website?style=plastic&?color=2b9348)](https://github.com/atulguptag/Django-eCommerce-Website/contributors)
[![Access Here](https://img.shields.io/badge/Access-Here-brightgreen?style=plastic)](https://footfusion.pythonanywhere.com/)
![GitHub License](https://img.shields.io/github/license/atulguptag/Django-eCommerce-Website?style=plastic&link=https%3A%2F%2Fgithub.com%2Fatulguptag%2FDjango-eCommerce-Website%2Fblob%2Fmain%2FLICENSE)

</div>

**FootFusion** is a full-fledged eCommerce website built with Django, a high-level Python web framework. It provides a robust, scalable, and user-friendly platform for a seamless online shopping experience. The project includes essential features like user authentication, product browsing, cart management, a secure checkout process with payment integration, and more.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Troubleshooting](#troubleshooting)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **User Authentication:** Secure user registration, login, password reset, and profile management.
- **Product Catalog:** Browse and search for products with detailed descriptions and images.
- **Shopping Cart:** Add, update, and remove items from the cart seamlessly.
- **Checkout Process:** A smooth checkout flow with an order summary and address management.
- **Payment Integration:** Integrated with Razorpay for secure online payments.
- **Order Management:** View order history and track status updates.
- **Responsive Design:** A mobile-friendly UI ensures a consistent experience across all devices.
- **Admin Panel:** Efficiently manage products, orders, and users through Django's admin interface.
- **URL-Based Images:** All images (products, categories, profiles) use URLs instead of file uploads, reducing storage requirements and enabling external image hosting.

## Technologies Used

- **Django:** A Python-based web framework for backend development.
- **HTML/CSS/JavaScript:** Frontend technologies for a responsive and interactive user interface.
- **Razorpay API:** A payment gateway integration for secure transactions.
- **Bootstrap:** A frontend framework for responsive design and UI components.

## Setup Instructions

To run this project locally, please follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/atulguptag/Django-eCommerce-Website.git
    cd Django-eCommerce-Website
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**

    - On Windows:
      ```bash
      .\venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

4.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure environment variables:**

    - Before running migrations, create a `.env` file in the project root. You can use `.env.example` as a template.
    - Add your `SECRET_KEY` and set `DEBUG=True` in the `.env` file.
    - Configure `BASE_URL` with your website URL (used for emails and payment callbacks):
      ```
      BASE_URL=http://127.0.0.1:8000  # For local development
      BASE_URL=https://yourdomain.com  # For production
      ```
    - Configure `ALLOWED_HOSTS` with your domain names (comma-separated, no spaces):
      ```
      ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
      ```
    - To generate a `SECRET_KEY`, run the following in your activated virtual environment:
      ```bash
      django-admin shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
      ```
    - Copy the output and paste it into your `.env` file (e.g., `SECRET_KEY=your-secret-key-here`).

6.  **Apply database migrations:**

    ```bash
    python manage.py migrate
    ```

7.  **Create a superuser (admin):**

    ```bash
    python manage.py createsuperuser
    ```

8.  **Start the development server:**

    ```bash
    python manage.py runserver
    ```

9.  **Access the application:**
    - Open your web browser and navigate to `http://127.0.0.1:8000/`.

## Troubleshooting

If you encounter issues during setup, here are some common problems and their solutions:

- **`Site.DoesNotExist` Error**: This error occurs when the `SITE_ID` in `ecomm/settings.py` does not match an entry in the database.

  - **Solution**: Ensure you have run the migrations (`python manage.py migrate`). If the error persists, inspect the `django_site` table in your database to find the correct ID for your site and update `SITE_ID` in `ecomm/settings.py` accordingly. Typically, this should be set to `1`.

- **`ModuleNotFoundError: No module named 'pkg_resources'`**: This indicates that the `setuptools` package is missing.

  - **Solution**: Install it using pip:
    ```bash
    pip install setuptools
    ```

- **Errors with `weasyprint` on macOS**: If you see an error like `OSError: cannot load library 'libgobject-2.0-0'`, it's because `weasyprint` is missing system-level dependencies.

  - **Solution**: Install the required libraries using Homebrew:
    ```bash
    brew install pango gdk-pixbuf libffi
    ```

- **Social Authentication Setup**: If you see errors on pages that require login, you may need to configure the social authentication settings.

  - **Solution**:

    1.  Navigate to the admin panel at `http://127.0.0.1:8000/admin/`.
    2.  Go to the "Social Accounts" -> "Social Applications" section.
    3.  Add a new social application (e.g., for Google) and provide your Client ID and Secret Key.

    ![Social Application Screenshot](Screenshots/google_auth-Change-social-application-Django-site-admin.png)

## Usage

- **Admin Panel:** Access the admin panel at `http://127.0.0.1:8000/admin/` to manage products, orders, and users.
- **Shopping:** Browse products, add items to the cart, proceed to checkout, and make payments using Razorpay.
- **User Profile:** Users can register, log in, reset their passwords, view their order history, and update their profiles.
- **Adding Images:** When adding products, categories, or updating your profile, use image URLs from external sources (e.g., image hosting services, CDNs, or direct URLs). The admin interface provides a URL input field for easy image management.

## Contributing

Contributions are welcome! Please fork this repository and create a pull request with your proposed features, enhancements, or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).

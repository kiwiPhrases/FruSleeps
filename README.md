# Fru Sleeps

This app is simply there to record who put the Fru to sleep and at what time.
You can then check the stats on Fru's sleeping patterns by parent and across time

The goal is ease of use so simple buttons to quickly record events
and minimal yet useful dashboard analytics


Author is Gene Burinskiy and all rights are reserved for now.

To-do list:

- allow for adding flexible quantity of caregivers up to, say, 5 entities
    - automatically add an "Other" caregiver for everyone
- track regular sleep and nap hours
    - if after 6pm, then default to sleep
    - if between 7am and 6pm, default to nap
- add e-mail confirmation
- add captcha to registration
- add time-out to sleep time confirmation page
- add documentation for
    - registration page: user is the child's name/nickname, email is unique
        - note, this allows only 1 child per e-mail
    - clarify that caregiver entry happens after child registration
    - buttons: they register the time of pressing and use that as an approximation for when the offspring fell asleep
- add more robust testing
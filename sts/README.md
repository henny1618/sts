**Project Name: sts**

**App Name: todo**

I work for the NOCC (Network Control Center) at Akamai and we work closely with another department called NIE (Network Infrastructure Engineering).  We delegate tickets to NIE with specific requests to reboot, reseat network cables, replace hardware, etc.  We started delegating these requests to NIE in JSON format, so they could process the large amount of requests programatically.  These requests are made in a ticket todo activity with the JSON and a human readable string.  This project for both the departments is called STS.

With the front end inteface of STS, you can create new NOCC observations for hardware components, and then you can then create new STS todos for each NOCC observation.  All components, observations, and todos are stored in a data base.  There is some validation when creating new or editing observations or todos.  In the future I would like to build some commandline tools to add todos to tickets.


Example todo object for disk replacement:

    NIE: Please replace the disk with serial 12345.

    {
        'type': 'STS-Automation',
        'version': '0.0',
        'comment': 'Disk Errors',
        'peace': 'no',
        'title': 'replace_disk',
        'rescue': 'no',
        'observations': {
            'component': {'disk'}
            'status': 'disk_error',
            'serial': '12345'
        }
    }


To run the app:

    cd sts
    python3 manage.py runserver


To create a new todo:

1.  Create a new superuser

        cd todo
        python3 manage.py createsuperuser

1.  Add all components via the [admin interface](http://127.0.0.1:8000/admin/todo/component/).  Log in using the super user account you just created.

1.  Create new NOCC observations for the components you just added.

1.  Create new STS todos for the observations you just added.


To run the unit tests:

    cd sts
    python3 manage.py test



To get all STS todos in JSON format from API.  In the future this will be more secure and work with commandline tools:

    make a GET request to /get_todos

Example response:

    [
        {
            "id": 4, 
            "version": 1, 
            "type": "STS-Automation", 
            "comment": "Disk Error", 
            "title": "replace_disk", 
            "peace": false, 
            "updated_at": "Dec 10 2021, 07:38 PM", 
            "created_at": "Dec 10 2021, 07:38 PM", 
            "observation": {
                "type": "NOCC-Automation", 
                "version": 1, "component": 
                "disk", "status": "disk_error", 
                "procedure": 2145, 
                "updated_at": "Dec 10 2021, 07:38 PM", 
                "created_at": "Dec 10 2021, 07:38 PM"
            }, 
            "human_readable": "Todo: replace_disk\n\nObservation: disk has disk_error.\n"
        }, 
        {
            "id": 5, 
            "version": 1, 
            "type": "STS-Automation", 
            "comment": "Unpingable Router", 
            "title": "reboot_router", 
            "peace": true, 
            "updated_at": "Dec 10 2021, 10:53 PM", 
            "created_at": "Dec 10 2021, 10:53 PM", 
            "observation": {
                "type": "NOCC-Automation", 
                "version": 0, 
                "component": "router", 
                "status": "unpingable", "
                procedure": 100, 
                "updated_at": "Dec 10 2021, 10:53 PM", 
                "created_at": "Dec 10 2021, 10:53 PM"
            }, 
            "human_readable": "Todo: reboot_router\n\nObservation: router has unpingable.\n"
        }
    ]


# Kwasi's-boilerplate

## Installation

*NOTE: Requires [virtualenv](http://virtualenv.readthedocs.org/en/latest/),
[virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) and
[Node.js](http://nodejs.org/).*

* Fork this repository.
* `$ git clone https://github.com/SingularityUniversity/impact-api.git
* `$ virtualenv mysite`
* `$ cd mysite/`
* `$ pip install -r requirements.txt`
* Set the following environment variables:
  * IMP_API_SECRET - 50 character randomly generated Django secret key
  * DW_RDS_DB_NAME - Name of the data warehouse database to connect to
  * DW_RDS_USERNAME - User to connect to the data warehouse as
  * DW_RDS_PASSWORD - Password to use to connect to data warehouse
  * DW_RDS_HOSTNAME - Data warehouse host
  * DW_RDS_PORT - Data warehouse port
* `$ python manage.py runserver`

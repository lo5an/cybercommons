Users and Persmissions
======================


## Django Admin Site

The Django admin comes with user and permissions functionality.

        URL - /api/admin

![Django Admin](images/djangoadmin.png)

### User Creation

The users are stored locally and passwords are stored within the database. Django comes with many different modules to extend the authentication functionality.

        URL - /api/admin/auth/user/
        
![User Creation](images/adduser.png)

### Permissions

The cyberCommons RESTful api provides permissions and groups:

1. Data Catalog

    * Catalog Creation
        * Catalog Admin
        * Create Catalog Collections
    * Collection Permissions
        * Add Permissions
        * Update Permission 
        * Safe Methods (Read) Permissions
2. Data Store

    * Catalog Creation
        * Data Store Admin
        * Create Database and Collections
    * Database and Collection Permissions
        * Add Permissions
            * When user create Database or Collection, its permission is default to public unless specify otherwise. 
        * Update Permission
            * Admin can grant or revoke permission to update data within a specific Collection.
            * This permission can be set for a specific user or a group of users.
        
        * Safe Methods (Read) Permissions
            * Any user can read the Database and Collections if they are public.
            * If a Database or Collection is private, only users with `superuser` permission can read the Database or Collection.

![User Permission](images/permission.png)    
### Database and Collection Visibility
This applies to both Data Catalog and Data Store and is set in the admin view. This setting controls who can see the Database or Collection.
* If Database or Collection is private, users can only see the Database or Collection if they have `superuser` permission.
* To update the visibility of a Database or Collection
    * If Database is set private, all Collections inside the Database will automatically be private and hidden from users without `superuser` permission.
    * If Database is set public, all Collections inside the Database will not automatically be public and can be updated as needed.
* To manually update the list of available Databases or Collections in the admin view, run the following command:
    * `make populate_db_perms`



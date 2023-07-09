# xPress API
**Developer: Gustaaf Milzink**

[Live Website]() coming soon...

This repository contains the Django REST Framework API for the xPress front end application.

[Repository]() coming soon...

[Live Website]() coming soon...

## Table of Contents
  - [User Stories](#user-stories)
  - [Database](#database)
  - [Technologies Used](#technologies-used)
  - [Validation](#validation)
  - [Testing](#testing)
  - [Credits](#credits)

## User Stories
The projects back-end section is focussed on it's administrative functionality and adresses a single user story:
- As site admin , I want to be able to create, edit and delete Users, Posts and Comments, so that I can have full control over the sites content and be able to remove any inapropriate content.

## Database

The following models were created to represent the database model structure of the application:
<img src="docs/db_models.png">


#### User Model
Contains information about the user.
Part of the Django allauth library.

- OneToOne relation with Profile model "owner" field.
- ForeignKey relation with Follower model "owner" field.
- ForeigKey relation with Follower model "followed" field.
- ForeignKey relation with Post model "owner" field.
- ForeignKey relation with Comment model "owner" field.
- ForeignKey relation with Like model "owner" field.

#### Profile Model
Contains the following fields:

"owner", "name", "avatar", "bio", "created_on" and "updated_on".
- OneToOne relation between "owner" field and User model "ID" field.
#### Follower Model
Contains the following fields:

"owner", "followed" and "created_on".
- ForeignKey relation between "owner" field and User model "ID" field.
- ForeignKey relation between "followed" field and User model "ID" field.

#### Post Model
Contains the following fields:

"owner", "title", "incclude_text", "text", "excerpt", "include_image", "image", "include_audio", "audio", "published", "created_on" and "updated_on".
- ForeignKey relation between "owner" field and User model "ID" field.

#### Comment Model   
Contains the following fields:

"owner", "post", "text", "created_on" and "updated_on".
- ForeignKey relation between "owner" field and User model "ID" field.
- ForeignKey relation between "post" field and Post model "ID" field.

#### Like model
Contains the following fields:

"owner", "post" and "created_on".
- ForeignKey relation between "owner" field and User model "ID" field.
- ForeignKey relation between "post" field and Post model "ID" field.

##### Back to [top](#table-of-contents)

## Technologies Used

### Languages & Frameworks

- Python
- Django

### Libraries & Tools

##### Back to [top](#table-of-contents)

## Validation

### Python Validation

## Testing

### Manual testing

### Automated testing

##### Back to [top](#table-of-contents)

## Credits

### Code

##### Back to [top](#table-of-contents)
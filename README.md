Todoistsorter 
=========
Image currently compiled for the following architectures (but could easily be compiled to others):
* `arm64v8`


What is Todoistsorter?
-----------------
Todoistsorter sorts (and capitalizes first letter) of tasks on a given Todoist task-list into sub-sections, based on where tasks with the same name was last _completed_.


Why I created this image?
-----------
* The image was created based on a my personal frustration when I would tell my Google Home to add something (e.g. milk) to my shopping list, which it would do using lowercase letters.
* This annoyed me, so I initially created a service to capitalize the first letter of the task.
* Then it occured to me that I would also like the things I added to be grouped logically based on their location in the supermarket I most often go to.
* So I extended the service to remember which section an item was last completed from (allowing the service to "learn"), so that it could move an item with the same name to the same section next time.

In short, what it does is:
1. Receives incoming webhook from Todoist
2. For added items: capitalized first letter (if not already done)
4. For added items: check if exists in database of previously known items
4a. If item is previously known it is moved to the last known section
4b. If item is not known, item is left where it is
5. For completed items: stores which section they were completed from



Prerequisites
-------------
* Todoist account (can be create here: https://todoist.com/users/showregister)
* Todoist app  (can be created here: https://developer.todoist.com/appconsole.html)
* * Setup "Webhooks callback URL" (url to reach the container)
* * Setup "Watched Events" (item:added, item:updated, item:completed)
* Container needs to be reachable from the internet (uses webhooks)
* API-token (can be found here: https://todoist.com/prefs/integrations, will look something like **be50z1p7zuisib8uj5unbe50z1p7zuisib8uj5un**
* Project (go to project using web-browser and see URL, will look something like this: **2F0123456789**)


Container parameters
-----------------
* `API-TOKEN` - Private API-token, can be retrieved from the "Integration" part of the settings in the Todoist web-interface (see above)
* `PROJECT` - ID of the project the project to monitor, can be retrieved from the url of the project when accessed through web-browser (see above section)



Docker Compose
--------------
~~~
version: "3.3"

services:

  todoistsorter:
    image: casperfrost/todoistsorter
    container_name: todoistsorter
    
    environment:
      - APITOKEN=**INSERT API-TOKEN HERE**
      - PROJECT=**INSERT PROJECT-ID HERE**

    ports:
      - 5000:5000
    restart: unless-stopped
~~~


Docker Run
--------------
~~~
docker run -p 5000:5000 --restart unless-stopped -e API-TOKEN=**INSERT API-TOKEN HERE**-e PROJECT=**INSERT PROJECT-ID HERE** casperfrost/todoistsorter
~~~


Feature wishlist
-----------
When I get time, these are the upcoming features I plan to develop:
- [x] Auto-capitalize first letter of items added to list
- [x] Sort item into last known section
- [ ] Allow for minor discrepancies in naming of an item
- [ ] Support for multi project monitoring
- [ ] Add note/label to indicate how item was added (e.g. voice or manual input)
- [ ] Translate list item to another language (for language training purposes)

Built Using
--------------
* Python v 3.8
* Alpine Linux
* Todoist Sync API v8
* SQLite3

Authors
----------
* **Casper Frost** - [CasperFrost](https://github.com/casperfrost)

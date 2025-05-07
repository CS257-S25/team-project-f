# StreamSearch Project Proposal
---

### Datasets

The datasets used in this project are 4 streaming service datasets with data on movies and TV shows from Netflix, Amazon Prime, Disney+, and Hulu.   
These datasets include the following key variables:  
~~~
Show ID 
Title  
Type (Movie/TV Show) 
Director 
Cast  
Country
Date Added
Release Year
Ratin 
Duration
Genre
~~~
We plan to analyze trends and create visualizations that compare streaming platforms across dimensions like genre, country of origin, representation, and platform-specific trends. We will also include features such as searching for titles with a specific actor, or determining where a specific title can be watched.

---

### Metadata

**Dataset: Netflix**  
	URL: [https://www.kaggle.com/datasets/shivamb/netflix-shows](https://www.kaggle.com/datasets/shivamb/netflix-shows)  
	Date Downloaded: 4/9/2025  
	Author: Shivam Bansal  
	Exact Name: Netflix Movies and TV Shows  
	Version: 5  
	Terms of Use: CC0  
	Suggested Citation:  
Netflix Movies and TV Shows Dataset. Kaggle. CC0: Public Domain License. Retrieved from [https://www.kaggle.com/](https://www.kaggle.com/).

**Dataset: Amazon Prime**  
URL: [https://www.kaggle.com/datasets/shivamb/amazon-prime-movies-and-tv-shows](https://www.kaggle.com/datasets/shivamb/amazon-prime-movies-and-tv-shows)  
Date Downloaded: 4/9/2025  
	Author: Shivam Bansal  
	Exact Name: Amazon Prime Movies and TV Shows  
	Version: 1  
	Terms of Use: CC0  
	Suggested Citation:  
Amazon Prime Movies and TV Shows Dataset. Kaggle. CC0: Public Domain License. Retrieved from [https://www.kaggle.com/](https://www.kaggle.com/).

**Dataset: Disney+**  
URL: [https://www.kaggle.com/datasets/shivamb/disney-movies-and-tv-shows](https://www.kaggle.com/datasets/shivamb/disney-movies-and-tv-shows)  
Date Downloaded: 4/9/2025  
	Author: Shivam Bansal  
	Exact Name: Disney+ Movies and TV Shows  
	Version: 2  
	Terms of Use: CC0  
	Suggested Citation:  
Disney+ Movies and TV Shows Dataset. Kaggle. CC0: Public Domain License. Retrieved from [https://www.kaggle.com/](https://www.kaggle.com/).

**Dataset: Hulu**  
	URL: [https://www.kaggle.com/datasets/shivamb/hulu-movies-and-tv-shows](https://www.kaggle.com/datasets/shivamb/hulu-movies-and-tv-shows)  
Date Downloaded: 4/9/2025  
	Author: Shivam Bansal  
	Exact Name: Hulu Movies and TV Shows  
	Version: 1  
	Terms of Use: CC0  
	Suggested Citation:  
Hulu Movies and TV Shows. Kaggle. CC0: Public Domain License. Retrieved from https://www.kaggle.com/.

---

### User Stories and Acceptance Criteria

**User Story 1: Search by Actor**  
As a fan of \[actor name\], I want to see a list of all the films and shows they appear in across streaming platforms, so I can easily find where to watch their work.

**Acceptance Criteria:**

* User can enter an actor’s name in a search bar.  
* System returns a list of titles the actor appears in.  
* Each result includes the title, streaming platform(s), type (movie or show), and year of release.

**User Story 2: Platform-Specific Browsing**  
As a \[streaming service\] user, I want to filter the database to show only content available on that platform, so I can browse what's available to me without sifting through other platforms.

**Acceptance Criteria:**

* User can select one or more streaming platforms via checkboxes or a dropdown menu.  
* Filter persists when combined with other search terms (e.g., actor, genre).  
* A “clear filters” button resets the selection.

**User Story 3: Explore Genre-Specific Content by Year**

As a \[genre\] fan, I want to browse all movies of that genre released after 2010 across all platforms, so I can discover new content that fits my interests.

**Acceptance Criteria:**

* User can select one or more genres (e.g., Animation).  
* User can enter a minimum release year.  
* System filters and displays all titles matching both criteria.  
* Each title includes the platform(s), description, and duration, ect.  
* No matching results triggers a “No titles found” message.

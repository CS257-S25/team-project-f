**User Stories and Acceptance Criteria**

**User Story 1: Search by Actor**  
As a fan of \[actor name\], I want to see a list of all the films and shows they appear in across streaming platforms, so I can easily find where to watch their work.

**Acceptance Criteria:**

* User can enter an actor’s name.  
* System returns a list of titles the actor appears in.  
* Each result includes the title.  

### **User Story 2: Explore Category-Specific Content by Year**

As a \[genre\] fan, I want to browse all movies of that category released after 2010 across all platforms, so I can discover new content that fits my interests.

**Acceptance Criteria:**

* User can select one or more categories (e.g., Animation).  
* User can enter a minimum release year.  
* System filters and displays all titles matching both criteria.  
* Located in the following functions:  
* ProductionCode/filter.py, `filter.py` → `Filter.filter_by_category()` and `Filter.filter_by_year_onward()`  
* `cl.py` → Command-line argument parsing with `--category` and `--year`  
* ProductionCode/filter.py, Output via `Filter.print_filtered_titles()` (or empty list \= "No titles found")

### **User Story 3: Advanced Search by Year, Actor, and Category**

### As a movie enthusiast, I want to search for titles by combining release year, actor, and category in a prioritized order, so that I can find highly specific content that aligns with my exact preferences.

**Acceptance Criteria:**

* User can input a minimum release year.  
* User can select one or more categories.  
* User can search by actor name.  
* User can stack the filters in a preferred hierarchical order (e.g., start with year, then filter by genre, then by actor).  
* System displays all titles matching all selected criteria in the order defined.  
* Located in the following functions:  
* ProductionCode/filter.py, `filter.py` → Combines `Filter.filter_by_year_onward()`, `filter_by_category()`, and `filter_by_actor()`  
* `cl.py` → Users can combine `--year`, `--category`, and `--actor` in any order  
* ProductionCode/filter.py, Output via `Filter.print_filtered_titles()`


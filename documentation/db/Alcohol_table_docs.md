﻿# Alcohol table documentation

# alcohol
 - alcohol_id serial
 - name varchar(50)
 - kind varchar(50)
	 - specifies aclohol kind (beer, vine, vodka, whiskey...)
 - rating float
 - type varchar(50)
	- the exact type of alcohol (f.e. for beer: IPA,APA...)
 - description varchar(1500)
 - region_id
 - alcohol_by_volume float
 - color varchar(50)
 - country varchar(50)
 - year integer
 - age integer
 - bitterness_ibu integer (beer)
	- The International Bitterness Units scale, or IBU, is used to approximately quantify the bitterness of beer. Measured on a scale from 0 to without upper limit.
 - srm float (beer)
	 - The Standard Reference Method is one of several systems modern brewers use to specify beer color.
 - extract float (beer)
	 - It describes the amount of sugar in the wort. Generally the higher the BLG the stronger, heavier and sweeter the beer
 - fermentation varchar (11) (beer)
	 - There are 4 types of fermentation top, bottom, spontaneous and mixed.
 - is_filtered boolean (beer)
 - is_pasteurized boolean (beer)
 - serving_temperature varchar(7)
 - manufacturer varchar(50)
 - image_path varchar(50)

# General

 - name varchar(50)
 - kind varchar(50)
     - specifies alcohol kind (beer, vine, vodka, whiskey...)
 - rating float
 - type
    - the exact type of alcohol (f.e. for beer: IPA,APA...)
 - description varchar(1500)
 - region_id
 - alcohol_by_volume float
 - color varchar(50)
 - country varchar(50)
 - year integer
 - age integer
 - temperature varchar(7)
 - manufacturer varchar(50)
 - vine_stock varchar(50)
 - image_path varchar(50)


### Many to many

 - food_name varchar(50)
 - aroma_name varchar(50)
 - flavour_name varchar(50)
 - ingredient_name varchar(50)

### One to many

 - region_name varchar(50)
    - country varchar (50)

	
# Beer

 - bitterness_ibu integer 
	- The International Bitterness Units scale, or IBU, is used to approximately quantify the bitterness of beer. Measured on a scale from 0 to without upper limit.
 - srm float
	 - The Standard Reference Method is one of several systems modern brewers use to specify beer color.
 - extract float
	 - It describes the amount of sugar in the wort. Generally the higher the BLG the stronger, heavier and sweeter the beer
 - fermentation varchar(11) (beer)
	 - There are 4 types of fermentation top, bottom, spontaneous and mixed.
 - is_filtered boolean (beer)
 - is_pasteurized boolean (beer)


# Wine
 - vine_stock varchar(50)

# Vodka

# Whiskey




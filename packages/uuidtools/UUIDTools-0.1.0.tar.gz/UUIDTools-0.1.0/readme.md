
# UUIDTools

UUIDTools is a tiny toolkit for working with uuids inside pandas dataframes or series,
this toolkit will help you to extract uuids from string (normalized and not normalized) databases,
and also permutate the ids into new ones preserving all the relations between diffrent tables.

## Requierments:

Python 3
uuid

## Installation:

> pip install UUIDTools

## Usage and use case: 

The usecase of this tool is mainly to copy SQL based tables with relations,
having two tables that you want to copy and export or reinsert but with different ids:

| ID                                   | parent ID                            |
|--------------------------------------|--------------------------------------|
| 2d452c66-7ede-403e-8b72-fe02d8bd24ed | d009237f-1899-421a-b2d1-21fa3f7c3103 |
| 2d452c66-7ede-403e-8b72-fe02d8bd24ed | edb66645-fef8-4359-b0e8-097868ed0747 |
| 9d044ff0-1c81-4bb8-b15b-33e60abfcc9c | f22fd493-fcd5-46ac-9014-3a4b1a96b4f2 |


| ID (Parent)                          | Name     |
|--------------------------------------|----------|
| d009237f-1899-421a-b2d1-21fa3f7c3103 | Person 1 |
| edb66645-fef8-4359-b0e8-097868ed0747 | Person 2 |
| f22fd493-fcd5-46ac-9014-3a4b1a96b4f2 | Person 3 |


If you need to generate new ids but you want to preserve the relations you can not
generate new random ids, this library will use the previous id as a seed for the next id generation

| IDs                                                                                                   |
|-------------------------------------------------------------------------------------------------------|
| d009237f-1899-421a-b2d1-21fa3f7c3103, something that is not id, d009237f-1899-421a-b2d1-21fa3f7c3103  |
| d980ce44-c8c3-4eb6-8e4c-1dbaed891c21                                                                  |
| f22fd493-fcd5-46ac-9014-3a4b1a96b4f2, d4b8fb9f-c048-4a60-8860-9b0edff0d838, bla bla                   |

Using this tool you can easily get the uuids contained:

| IDs                                                                        |
| {d009237f-1899-421a-b2d1-21fa3f7c3103}                                     |
| {d980ce44-c83c-4eb6-8e4c-1dbaed891c21}                                     |
| {f22fd493-fcd5-46ac-9014-3a4b1a96b4f2,d980ce44-c8c3-4eb6-8e4c-1dbaed891c21}|

Which is the set of the uuids above.



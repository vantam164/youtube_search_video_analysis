## Purpose
This repo is used to analyse videos on youtube related to searching keywords

## Approach
From searching keyword -> finding number of related videos, then analyse those videos based on tags, description ( current still only based on tags)

## Setup
1. Install docker and docker-compose (https://docs.docker.com/engine/install/) to run database mongodb
2. Install python package from requirement.txt

## Running
1. Run mongodb by command

`docker-compose up -d (need to go root project folder)
`

2. Run python CLI application with argument search keyword

`python3 entrypoint.py --search='{keyword}'
`

After running, excel report will be generated in root folder
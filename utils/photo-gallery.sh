#!/bin/bash
PHOTODB=$HOME/.empr/digikam

## Organize/Edit CMS photos
digikam --config $PHOTODB/photodb.ini --database-directory $PHOTODB

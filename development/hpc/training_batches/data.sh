#!/bin/bash
VAL="/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/val_chopped"
CROPIN="/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/crop_dominated/train"
FORESTIN="/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/forest_dominated/train"
SHRUBIN="/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/shrub_dominated/train"


CROPOUT="/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/crop_sites"
FORESTOUT="/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/forest_sites"
SHRUBOUT="/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/shrub_sites"

CROPSITES=(
    "29TQF"
    "30TWK"
    "30UYU"
    "31TBF"
    "31UFP"
    "32UNC"
    "33UWT"
    "33UXP"
    "34SEJ"
    "34TFL"
)

# FORESTSITES=(
#     "29SND"
#     "29TNE"
#     "30TTK"
#     "31TBF"
#     "31UFP"
#     "33VVG"
#     "33UWT"
#     "33VUF"
#     "33VUG"
#     "34SFF"
#     "34SEJ"
# )

FORESTSITES=(
    "33VXH"
)

SHRUBSITES=(
    "29SND"
    "29SPC"
    "29SQB"
    "29TPE"
    "29TQF"
    "30STJ"
    "30TTK"
    "30UYV"
    "31TBF"
    "32TML"
)

# for SITE in "${SHRUBSITES[@]}"; do
#     echo "$SITE"
#     PATH="$SHRUBOUT/$SITE"
#     /bin/mkdir -p "$PATH"
#     /bin/mkdir -p "$PATH/train"
#     /bin/cp -r "$VAL" "$PATH/"
#     /bin/cp -r "$SHRUBIN/$SITE" "$PATH/train/"
# done

# for SITE in "${CROPSITES[@]}"; do
#     echo "$SITE"
#     PATH="$CROPOUT/$SITE"
#     /bin/mkdir -p "$PATH"
#     /bin/mkdir -p "$PATH/train"
#     /bin/cp -r "$VAL" "$PATH/"
#     /bin/cp -r "$CROPIN/$SITE" "$PATH/train/"
# done

for SITE in "${FORESTSITES[@]}"; do
    echo "$SITE"
    PATH="$FORESTOUT/$SITE"
    /bin/mkdir -p "$PATH"
    /bin/mkdir -p "$PATH/train"
    /bin/cp -r "$VAL" "$PATH/"
    /bin/cp -r "$FORESTIN/$SITE" "$PATH/train/"
done


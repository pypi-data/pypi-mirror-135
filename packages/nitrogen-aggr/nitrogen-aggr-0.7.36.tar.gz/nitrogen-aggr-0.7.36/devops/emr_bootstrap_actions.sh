#!/usr/bin/env bash

read NITROGEN_ENV NITROGEN_VERSION CONFIG_FILE where <<<$@

[ "$NITROGEN_ENV" ] || {
 echo "Error: Incorrect number of command line parameters. NITROGEN_ENV is missing" >&2;
 echo "Correct format is: $0 [prod|qa|dev] NITROGEN_VERSION CONFIG_FILE" >&2;
 exit 1;
}

[ "$NITROGEN_VERSION" ] || {
 echo "Error: Incorrect number of command line parameters. NITROGEN_VERSION is missing" >&2;
 echo "Correct format is: $0 [prod|qa|dev] NITROGEN_VERSION CONFIG_FILE" >&2;
 exit 1;
}

[ "$CONFIG_FILE" ] || {
 echo "Error: Incorrect number of command line parameters. CONFIG_FILE is missing" >&2;
 echo "Correct format is: $0 [prod|qa|dev] NITROGEN_VERSION CONFIG_FILE" >&2;
 exit 1;
}

S3_CONFIG_PATH="s3://epi-nitrogen/$NITROGEN_ENV/conf/$CONFIG_FILE"
S3_DEV_CODE_PATH="s3://epi-nitrogen/dev/code/nitrogen-assembly-$NITROGEN_VERSION.jar"
GITHUB_API_TOKEN="483e33cb71dcdf18dc9d75c9547698445644f3ed"

get_github_release_asset() {
    # Script to download asset file from tag release using GitHub API v3.
    # See: http://stackoverflow.com/a/35688093/55075
    CWD="$(cd -P -- "$(dirname -- "$0")" && pwd -P)"

    type curl grep sed tr >&2

    # Validate settings.
    [ "$GITHUB_API_TOKEN" ] || { echo "Error: Please define GITHUB_API_TOKEN variable." >&2; exit 1; }
    [ "$TRACE" ] && set -x
    read owner repo tag name where <<<$@

    # Define variables.
    GH_API="https://api.github.com"
    GH_REPO="$GH_API/repos/$owner/$repo"
    GH_TAGS="$GH_REPO/releases/tags/$tag"
    AUTH="Authorization: token $GITHUB_API_TOKEN"
    WGET_ARGS="--content-disposition --auth-no-challenge --no-cookie"
    CURL_ARGS="-LJ#"

    # Validate token.
    curl -o /dev/null -sH "$AUTH" $GH_REPO || { echo "Error: Invalid repo, token or network issue!";  exit 1; }

    # Read asset tags.
    response=$(curl -sH "$AUTH" $GH_TAGS)
    # Get ID of the asset based on given name.
    eval $(echo "$response" | grep -C3 "name.:.\+$name" | grep -w id | tr : = | tr -cd '[[:alnum:]]=')
    #id=$(echo "$response" | jq --arg name "$name" '.assets[] | select(.name == $name).id') # If jq is installed, this can be used instead.
    [ "$id" ] || { echo "Error: Failed to get asset id, response: $response" | awk 'length($0)<100' >&2; exit 1; }
    GH_ASSET="$GH_REPO/releases/assets/$id"

    # Download asset file.
    echo "Downloading asset..." >&2
    curl $CURL_ARGS -H 'Accept: application/octet-stream' "$GH_ASSET?access_token=$GITHUB_API_TOKEN" -o $where
    echo "$0 done." >&2

}

if [ "$NITROGEN_ENV"  = "dev" ]
then
    aws s3 cp $S3_DEV_CODE_PATH /home/hadoop/nitrogen-assembly.jar
else
    get_github_release_asset EpisourceLLC nitrogen "v$NITROGEN_VERSION" "nitrogen-assembly-$NITROGEN_VERSION.jar" "/home/hadoop/nitrogen-assembly.jar"
fi

# Nitrogen Mappings
S3_NITROGEN_MAPPINGS="s3://epi-nitrogen/$NITROGEN_ENV/nitrogen_mappings.py"
S3_NITROGEN_MAPPINGS_CONFIG="s3://epi-nitrogen/$NITROGEN_ENV/nitrogen_mappings.json"
S3_NITROGEN_OUT="s3://epi-nitrogen/$NITROGEN_ENV/conf/out/"
aws s3 cp $S3_NITROGEN_MAPPINGS nitrogen_mappings.py
aws s3 cp $S3_NITROGEN_MAPPINGS_CONFIG nitrogen_mappings.json
sudo pip install requests
python nitrogen_mappings.py $NITROGEN_ENV $CONFIG_FILE
#aws s3 cp $S3_CONFIG_PATH infra.conf
cat nitrogen.conf <(echo) $CONFIG_FILE <(echo) infra.conf > alllocal.conf
# out
aws s3 cp alllocal.conf $S3_NITROGEN_OUT --sse
aws s3 cp infra.conf $S3_NITROGEN_OUT --sse
aws s3 cp nitrogen.conf $S3_NITROGEN_OUT --sse
aws s3 cp $CONFIG_FILE $S3_NITROGEN_OUT --sse

cp alllocal.conf /home/hadoop/local.conf
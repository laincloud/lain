#!/bin/bash

DOMAIN=$1

[[ -n "$DOMAIN" ]] || DOMAIN=lain.local

BOOTSTRAP_REG=$2

[[ -n "$BOOTSTRAP_REG" ]] || BOOTSTRAP_REG=registry.aliyuncs.com


IMAGES=(
    ipaddr-service:meta-1462790282-60f77d22799d8823ef771faef97897d60ca9c4b1
    ipaddr-service:release-1462790282-60f77d22799d8823ef771faef97897d60ca9c4b1
    ipaddr-resource:meta-1462784153-944220ca13e9aae08412875990686e18b71bff9e
    ipaddr-resource:release-1462784153-944220ca13e9aae08412875990686e18b71bff9e
    ipaddr-client:meta-1481187933-05da018887e967144f7d481b7ef160cb173973de
    ipaddr-client:release-1481187933-05da018887e967144f7d481b7ef160cb173973de
);


function pull_push()
{
    IMAGE=$1
    BOOTSTRAP_IMAGE="${BOOTSTRAP_REG}/laincloud/${IMAGE}"
    TARGET_IMAGE="registry.${DOMAIN}/${IMAGE}"
    sudo docker pull ${BOOTSTRAP_IMAGE}
    sudo docker tag ${BOOTSTRAP_IMAGE} ${TARGET_IMAGE}
    sudo docker push ${TARGET_IMAGE}
    sudo docker rmi ${BOOTSTRAP_IMAGE}
}

for i in "${IMAGES[@]}"
do
    pull_push $i
done

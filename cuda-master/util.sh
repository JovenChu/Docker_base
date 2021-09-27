retry() {
    counter=1
    maxtries=$1; shift;
    delay=$1; shift;
    echo RETRY: maxtries:$maxtries and delay:$delay
    while [[ $counter -le $maxtries ]]; do
        $@
        if [[ "$?" = "0" ]]; then
            break
        else
            >&2 echo "###############################################################################"
            >&2 echo Failed attempt $counter/$maxtries
            >&2 echo "###############################################################################"
            ((counter++))
            sleep $delay
        fi
    done
    if [[ $counter -gt $maxtries ]]; then
        >&2 echo "###############################################################################"
        >&2 echo RETRIES FAILED
        >&2 echo "###############################################################################"
        return 1
    fi
}

kitmaker_cleanup_webhook_success() {
    # echo "In here yo!"
    if [[ ! -z $KITMAKER && ! -z $TRIGGER ]]; then
        # set -x
        # echo "In here yo 2!"
        for tag_file in $(find . -iname "tag_manifest_*"); do
            # cat ${tag_file}
            cat ${tag_file} | grep -v nvidia.com >> UBER_TAG_MANIFEST
            cat ${tag_file} | grep nvidia.com >> image_name
        done
        echo "Preparing success json in kitmaker_cleanup_webhook_success()"
        echo ">>> BEGIN UBER_TAG_MANIFEST <<<"
        cat UBER_TAG_MANIFEST
        echo ">>> END UBER_TAG_MANIFEST <<<"
        export a_image_name=$(awk '/./{line=$0} END{print line}' image_name) # get the artifactory repo name
        # sed -i '$ d' UBER_TAG_MANIFEST # delete the last line containing the artifactory repo
        export json_data="{\"status\": \"success\", \"CI_PIPELINE_ID\": \"${CI_PIPELINE_ID}\", \"CI_JOB_ID\": \"${CI_JOB_ID}\", \"CI_COMMIT_SHORT_SHA\": \"${CI_COMMIT_SHORT_SHA}\", \"gitlab_pipeline_url\": \"${CI_PIPELINE_URL}\", \"image_name\": \"${a_image_name}\", \"tags\": $(cat UBER_TAG_MANIFEST | jq -R . | jq -s . | jq 'map(select(length > 0))' | jq -c .)}"
        echo curl -v -H "Content-Type: application/json" -d "${json_data}" "${WEBHOOK_URL}"
        curl -v -H "Content-Type: application/json" -d "${json_data}" "${WEBHOOK_URL}"
        # set +x
    fi
}

kitmaker_webhook_failed() {
    if [ ! -z $KITMAKER ] && [ ! -z $TRIGGER ]; then
        # if cat cmd_output | grep -q "error\|Error\|ERROR\|FAILED"; then
            # echo curl -v -H "Content-Type: application/json" -d "${json_data}" ${WEBHOOK_URL}
            # json_data="{\"status\": \"failed\", \"CI_PIPELINE_ID\": \"${CI_PIPELINE_ID}\", \"CI_JOB_ID\": \"${CI_JOB_ID}\", \ \"CI_COMMIT_SHORT_SHA\": \"${CI_COMMIT_SHORT_SHA}\", \"gitlab_pipeline_url\": \"${CI_PIPELINE_URL}\", \"cmd_output\": \"$(cat cmd_output)\"}"

        json_data=$(jq -n --arg status "failed" \
            --arg pipeline_id "${CI_PIPELINE_ID}" \
            --arg job_id "${CI_JOB_ID}" \
            --arg ci_commit "${CI_COMMIT_SHORT_SHA}" \
            --arg pipeline_url "${CI_PIPELINE_URL}" \
            '{status: $status, pipeline_id: $pipeline_id, job_id: $job_id, ci_commit: $ci_commit, pipeline_url: $pipeline_url}')

                # FIXME: It is very helpful to show the error output in jenkins, but gitlab does not make it easy to get this
                # if a stage fails....
                # --arg cmd_output "$(cat cmd_output)" \
                # '{status: $status, pipeline_id: $pipeline_id, job_id: $job_id, ci_commit: $ci_commit, pipeline_url: $pipeline_url, cmd_output: $cmd_output}')

        echo "json_data: $(echo ${json_data} | jq)"
        curl -H "Content-Type: application/json" -d "${json_data}" ${WEBHOOK_URL}
        # exit 1
        # elif cat cmd_output | grep -q "DONE"; then
        #     echo "Seems the last 'run_cmd' command succeeded! Not calling webhook."
        # fi
    fi
    # If this function is called, it should always fail
    # ...but not in the new multi-arch configuration. Keeping this for when we fix error reporting
    # exit 1
}

run_cmd() {
    printf "===== %s\n\n" "Running command:"
    printf "%s " "${@}"
    printf "\n\n"
    printf "===== Output: \n\n"
    # echo -e "$@" | source /dev/stdin 2>&1 | tee cmd_output
    echo -e "$@" | source /dev/stdin 2>&1
    run_cmd_return=$?
    echo
    printf "===== Command returned: %s\n\n" "${run_cmd_return}"
    return $run_cmd_return
}

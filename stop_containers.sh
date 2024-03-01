
# command to run 
# docker ps --format "{{.ID}}\t{{.Names}}" | grep "edo_t1_recon" | awk '{print $1}' > container_info.txt
# container_ids=($(docker ps --format "{{.ID}}\t{{.Names}}" | grep "edo_t1_recon" | awk '{print $1}'))
container_ids=(
"d0505fd956d2"   
"f204ec8f5b31"   
"0bbfae664987"   
"09146ea7971f"   
"0ed642f4c3e5"   
"e94a5d9bd2b4"   
)

# Loop through the container IDs and stop and remove each container
for container_id in "${container_ids[@]}"; do
    echo "container to remove: $container_id"
    docker stop "$container_id"
    # docker rm "$container_id"
done

# Loop through the container IDs and stop and remove each container
# for image_id in "${image_ids[@]}"; do
#     echo "removaing image: $image_id"
#     docker rmi "$image_id" -f
#     # docker rm "$container_id"
# done
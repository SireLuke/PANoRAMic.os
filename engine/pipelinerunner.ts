export function pipelineRunner(world, pipeline, subsystems) {
    for (const step of pipeline) {
        if (subsystems[step]) {
            world[step] = subsystems[step](world);
        }
    }
    return world;
}
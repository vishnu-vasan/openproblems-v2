workflow auto {
  findStates(params, meta.config)
    | meta.workflow.run(
      auto: [publish: "state"]
    )
}

workflow run_wf {
  take:
  input_ch

  main:
  output_ch = input_ch

    // TODO: check schema based on the values in `config`
    // instead of having to provide a separate schema file
    | check_dataset_schema.run(
      fromState: [
        "input": "input",
        "schema": "dataset_schema"
      ],
      args: [
        "stop_on_error": false,
        "checks": null
      ],
      toState: ["dataset": "output"]
    )

    // remove datasets which didn't pass the schema check
    | filter { id, state ->
      state.dataset != null
    }

    | process_dataset.run(
      fromState: [input: "dataset"],
      toState: [
        output_dataset: "output_dataset",
        output_solution: "output_solution"
      ]
    )

    // only output the files for which an output file was specified
    | setState(["output_dataset", "output_solution"])

  emit:
  output_ch
}
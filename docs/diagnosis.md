# Training run diagnosis

`diagnose(trace)` accepts a sequence of two or more finite `(loss, gradient)`
pairs. Raise `ValueError` for a short trace or any nonfinite value. Compare the
last loss to the first. An increase yields `reduce learning rate`. A decrease
yields `loss decreasing`. A flat loss yields `inspect gradient` when the last
gradient is zero and `check learning rate` otherwise.

For `training_report(rate)`, start a scalar parameter at zero. At each of three
steps, broadcast it over targets 2 and 4 to compute residuals, sum the squares,
and obtain the parameter gradient from your graph. Record the loss and gradient
before updating the parameter. Use your cosine retriever to select one training
note from a relevant note and an unrelated note. Pass the selected note as
document data.

Send your mock model through the earlier parser, tool dispatcher and runtime.
Its first request attempts the forbidden `change` tool with ID `write`. Its next
request uses the authorized `inspect` tool with ID `read` and no arguments.
The inspection tool classifies the trace. The model returns that tool result
as its final text. Return the complete runtime report. Register both tools so
permission determines whether the change runs.

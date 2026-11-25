"""Reference and wrong guesses in the order of each method's blanks."""

GuessSet = tuple[object, ...]


ANSWERS: dict[str, dict[str, tuple[GuessSet, GuessSet]]] = {
    "python_references": {
        "test_rebinding_a_name_leaves_the_other_name_alone": (
            (['queued'], False),
            (['done'], True),
        ),
        "test_a_shallow_copy_preserves_repeated_child_references": (
            (False, True, 3),
            (False, False, 1),
        ),
        "test_deep_copy_detaches_a_container_and_keeps_shared_children": (
            (False, True, ['marker']),
            (False, False, ['marker', 'new']),
        ),
        "test_a_copy_can_point_to_itself": (
            (False, True, False),
            (True, False, True),
        ),
    },
    "python_closures": {
        "test_defaults_capture_values_while_closures_read_cells": (
            (5, 2),
            (2, 5),
        ),
        "test_a_key_can_ignore_keyword_order_without_ignoring_values": (
            (False, True, False),
            (True, True, True),
        ),
        "test_wraps_exposes_the_original_name_and_description": (
            ('dosage', 'Scale the measurement.', True),
            ('traced', None, False),
        ),
    },
    "python_attributes": {
        "test_an_inherited_property_uses_the_receiving_instance": (
            (273, 283, True),
            (273, 273, False),
        ),
        "test_set_name_observes_which_attribute_is_bound": (
            ('pressure', True),
            ('field', False),
        ),
        "test_a_descriptor_setter_can_validate_before_storing": (
            ('rejected', 4),
            ('accepted', True),
        ),
    },
    "python_streams": {
        "test_constructing_a_generator_leaves_work_pending": (
            ([], 4, [4], (8, 12)),
            ([4], 4, [4, 8, 12], (4, 8, 12)),
        ),
        "test_freezing_a_moving_buffer_keeps_an_earlier_window": (
            ((1, 2), (2, 3)),
            ((2, 3), (1, 2, 3)),
        ),
        "test_taking_matches_consumes_rejected_items_along_the_way": (
            ([3], 4, [5]),
            ([3], 2, [3, 5]),
        ),
    },
    "python_scheduler": {
        "test_gather_preserves_input_order_after_out_of_order_completion": (
            (['second', 'first'], ['first', 'second']),
            (['first', 'second'], ['second', 'first']),
        ),
        "test_cancelling_a_running_coroutine_executes_finally": (
            (['cleanup', 'cancelled'],),
            (['cancelled', 'cleanup'],),
        ),
        "test_gather_can_report_an_error_without_losing_other_results": (
            ('ValueError', 7),
            ('CancelledError', None),
        ),
    },
    "python_rest_service": {
        "test_creation_and_lookup_have_different_response_metadata": (
            (False, None, True),
            (True, '/jobs/3', False),
        ),
        "test_replacing_the_registry_entry_keeps_a_stored_creation_response": (
            ('queued', 'complete', False),
            ('complete', 'complete', True),
        ),
        "test_a_request_key_can_refer_to_one_original_input": (
            ('refresh', 'refresh', 1),
            ('refresh', 'reindex', 2),
        ),
    },
    "deep_learning_linear": {
        "test_basis_vectors_pick_out_columns": (
            ([2, 3], [5, 7]),
            ([2, 5], [3, 7]),
        ),
        "test_rows_dot_columns_not_other_rows": (
            ((2, 3), 8, 110),
            ((2, 10), 22, 89),
        ),
        "test_zip_truncates_unless_we_require_equal_lengths": (
            ([(2, 3)], 'ValueError'),
            ([(2, 3), (4, 0)], 'accepted'),
        ),
    },
    "deep_learning_precision": {
        "test_floating_point_addition_can_erase_a_small_increment": (
            (0.0, 1.0),
            (1.0, 1.0),
        ),
        "test_the_log_loss_can_survive_probability_underflow": (
            (0.0, 1000.0),
            (0.0, float("inf")),
        ),
        "test_only_the_target_coordinate_gets_the_indicator": (
            (0.25, -0.5, 0.0),
            (-0.75, -0.5, -2.0),
        ),
    },
    "deep_learning_autodiff": {
        "test_a_shared_operand_has_two_local_derivatives": (
            (12.0, 24.0),
            (12.0, 12.0),
        ),
        "test_a_branch_can_add_two_different_contributions_to_one_node": (
            (10, 7),
            (10, 3),
        ),
        "test_the_backward_seed_scales_every_contribution": (
            ((2.0, -5.0), (-4.0, 10.0)),
            ((2.0, -5.0), (2.0, -5.0)),
        ),
    },
    "deep_learning_tensor": {
        "test_a_row_can_be_reused_for_each_column_value": (
            ([2, 2], [13, 23]),
            ([2, 1], [23]),
        ),
        "test_a_single_input_can_contribute_to_every_output_row": (
            ([8, 12, 20], 10),
            ([8, 12, 20], 5),
        ),
        "test_reducing_by_row_and_by_column_preserves_different_axes": (
            ([9, 18], [7, 9, 11]),
            ([7, 9, 11], [9, 18]),
        ),
    },
    "deep_learning_attention": {
        "test_a_mask_is_applied_before_choosing_the_normalizer": (
            (3.0, 2.0),
            (1000.0, 0.0),
        ),
        "test_a_weighted_value_combines_coordinates_independently": (
            (5.0, 1.0),
            (6.0, 0.0),
        ),
        "test_each_causal_row_exposes_a_different_prefix": (
            ([True, False, False, False], [True, True, True, False], 4),
            ([False, False, False, False], [True, True, False, False], 3),
        ),
    },
    "agents_protocol": {
        "test_valid_json_can_still_have_the_wrong_shape": (
            ('list', False),
            ('dict', True),
        ),
        "test_strictly_finite_arguments_need_validation_after_parsing": (
            (True, False),
            (True, True),
        ),
        "test_final_text_is_a_string_even_if_it_looks_like_a_message": (
            ('str', 'final'),
            ('dict', 'call'),
        ),
    },
    "agents_tools": {
        "test_registration_and_permission_are_independent": (
            (False, False, True),
            (True, True, True),
        ),
        "test_an_extra_argument_is_a_schema_mismatch": (
            (True, False),
            (True, True),
        ),
        "test_building_keyword_arguments_does_not_invoke_a_tool": (
            ([], 30, [3]),
            ([3], 30, [3, 3]),
        ),
    },
    "agents_retrieval": {
        "test_positive_rescaling_does_not_change_direction": (
            ([0.6, 0.8], [0.6, 0.8], [-0.6, -0.8]),
            ([0.6, 0.8], [1.2, 1.6], [0.6, 0.8]),
        ),
        "test_ranking_ties_can_be_broken_without_using_document_text": (
            (['a', 'c', 'b'], 'last'),
            (['c', 'a', 'b'], 'first'),
        ),
        "test_joining_evidence_uses_space_for_separators": (
            (6, 7),
            (6, 6),
        ),
    },
    "agents_planning": {
        "test_repeated_edges_should_only_count_one_prerequisite": (
            (3, 2),
            (3, 3),
        ),
        "test_newly_ready_work_can_move_ahead_of_waiting_work": (
            ('b', 'a', 'z'),
            ('b', 'z', 'a'),
        ),
        "test_one_completed_dependency_might_not_release_a_job": (
            (False, True),
            (True, True),
        ),
    },
    "agents_runtime": {
        "test_canonical_arguments_ignore_key_order_and_distinguish_booleans": (
            (True, True, False),
            (True, True, True),
        ),
        "test_a_model_can_mutate_its_copy_without_updating_the_runtime": (
            ('read', True),
            ('changed', False),
        ),
        "test_characters_and_bytes_are_different_budget_units": (
            (7, 9),
            (7, 7),
        ),
    },
    "agents_providers": {
        "test_input_and_output_counters_measure_different_parts_of_usage": (
            (False, True),
            (False, False),
        ),
        "test_a_boolean_can_look_like_a_token_count": (
            (7, False),
            (7, True),
        ),
        "test_the_exception_retains_status_for_the_routing_decision": (
            ([429, 503], 1),
            ([401, 429, 503], 0),
        ),
    },
    "agents_workflow_graph": {
        "test_a_frozen_record_can_still_contain_a_mutable_dictionary": (
            (1, 1, True),
            (1, 0, False),
        ),
        "test_a_transition_validates_its_route_before_committing": (
            (1, {'count': 0}, 'start'),
            (2, {'count': 7}, 'later'),
        ),
        "test_pausing_preserves_the_next_node": (
            (False, 'next', 3),
            (True, None, 0),
        ),
    },
    "agents_grounded_qa": {
        "test_a_total_budget_differs_from_a_per_document_limit": (
            (['a', 'b', 'c'], ['a', 'c']),
            (['a', 'b', 'c'], ['a', 'b', 'c']),
        ),
        "test_a_set_check_alone_cannot_detect_duplicate_citations": (
            (True, False),
            (False, False),
        ),
        "test_citations_can_match_when_rendering_order_differs": (
            (False, True),
            (True, True),
        ),
    },
    "agents_webhooks": {
        "test_a_timestamp_is_part_of_the_signed_bytes": (
            (False, True),
            (True, True),
        ),
        "test_the_time_window_applies_to_past_and_future_deliveries": (
            ([False, True, True, False], 2),
            ([False, True, True, True], 3),
        ),
        "test_an_existing_receipt_keeps_the_original_delivery_result": (
            (False, 9),
            (True, 9),
        ),
    },
    "cross_track_diagnosis": {
        "test_a_shared_weight_receives_a_contribution_from_each_target": (
            (20.0, -12.0),
            (20.0, -8.0),
        ),
        "test_a_large_step_can_increase_loss_despite_a_nonzero_gradient": (
            (2.25, True),
            (2.25, False),
        ),
        "test_a_flat_loss_can_hide_either_a_zero_rate_or_a_zero_gradient": (
            (True, False),
            (True, True),
        ),
    },
}

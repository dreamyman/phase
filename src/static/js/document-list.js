jQuery(function($) {
    var queryparams = new QueryParams();

    // initialize minimal query parameters
    queryparams.fromString($('#table-filters').serialize());

    /* Deal with download buttons */
    $('.navbar-form button[type=button]').click(function () {
        var btn = $(this),
            format = btn.data('format'),
            revisions = btn.data('revisions');
        if (format !== undefined) {
            $('#id_format').val(format);
        } else if (revisions !== undefined) {
            $('#id_revisions').val(revisions);
        }
    });


    ///* document list *///

    /* Dealing with addition/removal of favorites */
    var updateDocumentNumber = function(display, total) {
        $("#display-results").text(display);
        $("#total-results").text(total);
    };

    var favoriteDocument = function() {
        $('#documents tbody').on('click', '.columnfavorite', function(e) {
            $(this).children().favbystar({
                userId: config.userId,
                csrfToken: config.csrfToken,
                createUrl: config.createUrl,
                deleteUrl: config.deleteUrl
            });
        });
    };

    /* Initializing the datatable */
    var datatable = $('#documents').datatable({
        filterUrl: config.filterUrl,
        updated: function(rows, params) {
            params && params['total'] == rows.length ? $('.pagination a').hide() : $('.pagination a').show();
            // update headers information
            if (params) {
                updateDocumentNumber(params['display'], params['total']);
            } else {
                updateDocumentNumber(config.numItemsPerPage, config.totalItems);
            }
        }
    });

    datatable.draw(tableData);

    /* Filter datatable's results given selected form's filters */
    var serializeTable = function(evt) {
        var parameters = $('#table-filters').serializeArray();
        /* Update the pagination link */
        queryparams.fromString($('#table-filters').serialize());
        datatable.update(queryparams.data, {
            total: config.totalItems
        });
        $(this).siblings('i').css('display', 'inline-block');
        evt.preventDefault();
    };

    $("#table-filters select").on('change', serializeTable);
    $("#table-filters input").on('afterkeyup', serializeTable);
    $("#table-filters i").on('click', function(evt) {
        $(this).siblings('select,input:text').val('');
        serializeTable(evt);
        $(this).hide();
    });
    $("#documents th:not(#columnselect):not(#columnfavorite)").on('click', function(evt) {
        var $this = $(this);
        var sortBy = $this.data("sortby");
        var $sortBy = $('#id_sort_by');
        var direction = (sortBy == $sortBy.val()) ? '-' : '';
        $('#id_sort_by').val(direction + sortBy);
        $i = $this.children();
        $i.is('[class*=glyphicon-chevron-]') ? $i.toggleClass("glyphicon-chevron-up").toggleClass("glyphicon-chevron-down") : $i.addClass('glyphicon-chevron-down');
        $("#documents th i").not($i).removeClass("glyphicon-chevron-down glyphicon-chevron-up");
        serializeTable(evt);
    });

    /* Reseting the filtering form and thus the table's results */
    $('#resetForm').on('click', function(evt) {
        $('#table-filters').find('input:text, select').val('');
        $('#filters').find('select').val('');
        serializeTable(evt);
        $("#table-filters i").each(function(evt) {
            $(this).hide();
        });
    });

    /* select documents */

    // select rows
    var selectableRow = function() {
        var $row;
        var form = document.querySelector('.navbar-form');
        $("#documents tbody").on('change', 'input[type=checkbox]', function(e) {
            $row = $(this).closest('tr');
            var documentId = $row.data('document-id');
            $('.navbar-form .disabled').removeClass('disabled');
            if ($(this).is(':checked')) {
                $row.addClass('selected');
                var input = document.createElement('input');
                input.id = "document-id-"+documentId;
                input.name = "document_ids";
                input.type = "hidden";
                input.value = documentId;
                form.appendChild(input);
            } else {
                $row.removeClass('selected');
                $(".navbar-form input#document-id-"+documentId).remove();
            }
        });
    };

    // select/deselect all rows
    var selected, checkbox;
    $('#select-all').on('change', function(e) {
        selected = $(this).is(':checked');
        checkbox = $("#documents tbody input[type=checkbox]");
        checkbox.prop('checked', selected);
        checkbox.trigger('change');
    });

    /* browse documents if you click on table cells */

    var clickableRow = function() {
        $("#documents tbody").on('click', 'td:not(.columnselect):not(.columnfavorite)', function(e) {
            window.location = config.detailUrl.replace(
                'documentNumber',
                $(this).parent().data('document-number'));
        });
    };

    /* Shortcut to refresh all row's behavior when content is appened */
    var rowBehavior = function() {
        clickableRow();
        selectableRow();
        favoriteDocument();
    };
    rowBehavior();

    // click on next page appends rows to table
    $('.pagination a').on('click', function(evt) {
        var d = queryparams.data;
        // increment 'start' parameter to get next page
        d['start'] = parseInt(d['start'], 10) + parseInt(d['length'], 10);
        queryparams.update(d);
        // update the table
        datatable.append(queryparams.data);
        evt.preventDefault();
    });

    // reaching "next" button simulate a click
    $('.pagination a').on('inview', function(event, isInView, visiblePartX, visiblePartY) {
        if (isInView) {
            $(this).trigger('click');
        }
    });

    // off canvas
    $('[data-toggle=offcanvas]').click(function() {
        var row = $('.row-offcanvas');
        row.toggleClass('active');

        var icon = $(this).find('span.glyphicon');
        if (row.hasClass('active')) {
            icon.removeClass('glyphicon-arrow-left');
            icon.addClass('glyphicon-arrow-right');
        } else {
            icon.addClass('glyphicon-arrow-left');
            icon.removeClass('glyphicon-arrow-right');
        }
    });
});

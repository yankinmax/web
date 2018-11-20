Use `url` widget as you do usually, then add an extra parameter `text_field`
to indicate which field (present in the view already) must be used for the anchor text.


.. code-block:: xml

    <field name="some_url" widget="url" text_field="another_field" />

M2O fields are supported: `display_name` is used automatically.

def get_options_metaclass(
    class_name: str, meta_attr: str, default_meta_attr: str
) -> type:
    """
    Helpers that implements the appropriate metaclass for the Meta-DefaultMeta pattern.

    :param class_name: Name of the class being created.
    :param meta_attr: Name of the attribute that will hold the class with the metadata.
    :param default_meta_attr: Name of the attribute that will hold the class with the default values.
    :return: Metaclass to be used on other classes.
    """

    class Metaclass(type):
        def __new__(mcs, name, bases, attrs, **kwargs):
            cls_meta = attrs.get(meta_attr, None)
            default_meta_cls = attrs.get(default_meta_attr, None)

            # default_meta_attr should never be a subclass of another default_meta_attr class
            # default metas are inherited, non default ones are not
            default_meta_bases = (
                getattr(base, default_meta_attr)
                for base in bases
                if hasattr(base, default_meta_attr)
            )

            cls = super().__new__(mcs, name, bases, attrs, **kwargs)

            default_meta_cls = mcs.get_default_meta_subclass(
                default_meta_cls, default_meta_bases
            )
            meta_class = mcs.get_meta_subclass(cls_meta, default_meta_cls)

            setattr(cls, default_meta_attr, default_meta_cls)
            setattr(cls, meta_attr, meta_class)

            return cls

        @classmethod
        def get_default_meta_subclass(mcs, cls_default_meta, default_meta_bases):
            if cls_default_meta is not None:
                bases = (cls_default_meta, *default_meta_bases)
            else:
                bases = tuple(default_meta_bases)

            return type(default_meta_attr, bases, {})

        @classmethod
        def get_meta_subclass(mcs, cls_meta: type, default_meta_cls: type):
            """
            Returns a Meta with the default values

            Args:
                cls_meta: Class specific Meta class
                default_meta_cls: Class specific Default Meta class
            Returns:
                A new object with the proper Meta class
            """

            # Custom Meta should be at the beginning
            if cls_meta is not None:
                bases = (cls_meta, default_meta_cls)
            else:
                bases = (default_meta_cls,)

            return type(meta_attr, bases, {})

    return type(class_name, (Metaclass,), {})

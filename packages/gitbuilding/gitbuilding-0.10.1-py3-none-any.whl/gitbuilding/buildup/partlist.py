'''
This submodule contains functionality to handle lists of parts in the BuildUp
documentation.
'''

import logging
from gitbuilding.buildup.basepart import Part
from gitbuilding.buildup.parts import UsedPart
from gitbuilding.buildup.parts import CreatedPart

_LOGGER = logging.getLogger('BuildUp')
class PartList:
    """
    PartLists are lists of Part objects. They have functions that allow them to
    safely add parts and to be merged.
    """

    def __init__(self, config):

        self._parts = []
        self._config = config

    def __getitem__(self, ind):
        return self._parts[ind]

    def __setitem__(self, ind, part):
        if not isinstance(part, Part):
            raise TypeError("Can only store Part objects in a PartList")
        self._parts[ind] = part

    def __len__(self):
        return len(self._parts)

    def _append(self, part):
        """
        Appends a new part into the list, this function is used by count_link
        if no matching part exists.
        """

        if not isinstance(part, Part):
            raise TypeError("Can only append Part objects to a PartList")

        self._parts.append(part)

    def index(self, part):
        """
        Works as index for a list but uses the __eq__ method of Part objects
        in the part list
        """
        return self._parts.index(part)

    def getpart(self, part):
        """
        Returns the part object from the list that matches input "part"
        uses the __eq__ method of Parts, so this input could be a Part
        object or a string
        """
        if part in self._parts:
            return self._parts[self.index(part)]
        return None

    @property
    def used_parts(self):
        """
        Only the parts that are used not the ones that were created.
        """
        return [part for part in self._parts if isinstance(part, UsedPart)]

    def merge(self, inputlist):
        """
        Merges in another partlist
        """
        if not isinstance(inputlist, PartList):
            raise TypeError("Can only merge a PartList to another PartList")
        for part in inputlist:
            matching_part = self.getpart(part)
            if matching_part is None:
                self._append(part.replicate())
            else:
                matching_part.combine(part)

    def count_link(self, link):
        """
        Takes the information from a link and stores it in the coresponding UsedPart
        object so the information is counted when the bill of materials is created
        If it a matching doesn't exist, one is created.
        """

        part = self.getpart(link)
        if part is None:
            if link.is_output:
                self._append(CreatedPart(link))
            else:
                self._append(UsedPart(link, self._config))
        else:
            part.count(link)

    def link_refs_md(self, url_translator, excludelist=None):
        """
        Returns the markdown link reference for each part. All links are translated
        with the url_translator. Parts can be excluded using the excludelist.
        """
        linktext = ""

        if excludelist is None:
            excludelist = []

        for part in self.used_parts:
            if part not in excludelist:
                linktext += f"{part.link_ref_md(url_translator)}\n"
        return linktext

    def bom_md(self, title, url_translator, divide=True, exclude_refs=None, intro=None):
        """
        Creates the bill of materials in markdown format.
        Can set whether it also includes the link references for each
        part, and whether they are divided by categories

        The `divide` argument means the bill of materials will have headings
        for each of the part categories when set to `True` (the default).
        """
        sorted_parts = sorted(self.used_parts)
        bom_text = ""
        if title != "":
            bom_text += f"{title}\n\n"
        if intro is not None:
            bom_text += intro
            bom_text += "\n\n"
        # Loop through parts and put quantities and names in md
        if divide:
            for category in self._config.categories:
                catname = self._config.categories[category].display_name
                first = True
                for part in sorted_parts:
                    if part.category == category:
                        if first:
                            first = False
                            bom_text += f"\n\n### {catname}\n\n"

                        bom_text += part.bom_line(url_translator)
        else:
            for part in sorted_parts:
                bom_text += part.bom_line(url_translator)
        bom_text += self.link_refs_md(url_translator, exclude_refs)
        bom_text += "\n\n"
        return bom_text

    def bom_csv(self, doc):
        """
        Outputs a bill of materials in character-separated values format.
        Tab-separated is the only option for now.
        """
        sorted_parts = sorted(self.used_parts)
        entries = []
        max_products = 0
        for part in sorted_parts:
            part_data = part.get_part_data(doc)
            entries.append((part, part_data))
            if part_data is not None:
                num_products = len(part_data.product_list)
                if num_products > max_products:
                    max_products = num_products

        csv = ""
        headings = ["Name in documentation", "Qty", "Full Name"]
        for n in range(max_products):
            headings += [f"Supplier {n+1}", "Part No", "Link"]
        csv += "\t".join(headings)
        csv += "\n"

        for part, part_data in entries:
            #somewhat ugly double list comprehension to flatten the list of tuples into a flat list
            if part_data is None:
                flat_products = []
                part_data_name = ""
            else:
                flat_products = [item for product in part_data.product_list for item in product]
                part_data_name = part_data.name
            #calculate extra columns to pad row
            extra_cols = 3*max_products - len(flat_products)
            row = [part.name, str(part.qty), part_data_name] + flat_products + ['']*extra_cols
            csv += "\t".join(row)
            csv += "\n"
        return csv

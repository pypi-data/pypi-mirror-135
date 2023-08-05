#!/usr/bin/env python3.8
# coding: latin-1

# (c) Massachusetts Institute of Technology 2015-2018
# (c) Brian Teague 2018-2022
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
cytoflowgui.editors.vertical_notebook
-------------------------------------

The model for `cytoflowgui.editors.vertical_notebook_editor.VerticalNotebookEditor`.

"""

# for local debugging
if __name__ == '__main__':
    from traits.etsconfig.api import ETSConfig
    ETSConfig.toolkit = 'qt4'

    import os
    os.environ['TRAITS_DEBUG'] = "1"

from pyface.qt import QtGui, QtCore
from pyface.api import ImageResource

from traits.api import (HasTraits, HasPrivateTraits, Instance, List, Str, Bool, 
                        Property, Any, cached_property, Int, on_trait_change)

from traitsui.api import UI, Editor

class VerticalNotebookPage(HasPrivateTraits):
    """ 
    A class representing a vertical page within a notebook. 
    """

    #-- Public Traits --------------------------------------------------------

    name = Str
    """The name of the page (displayed on its 'tab')"""

    description = Str
    """ The description of the page (displayed in smaller text in the button)"""
    
    ui = Instance(UI)
    """The Traits UI associated with this page """

    data = Any
    """Optional client data associated with the page """

    name_object = Instance(HasTraits)
    """The HasTraits object whose trait we look at to set the page name"""

    name_object_trait = Str
    """The name of the *name_object* trait that signals a page name change"""

    description_object = Instance(HasTraits)
    """The HasTraits object whose trait we look at to set the page description"""

    description_object_trait = Str
    """The name of the *description_object* trait that signals a page description change"""

    icon = Str('ok')
    """The icon for the page button -- a Str that is the name of an ImageResource"""

    icon_object = Instance(HasTraits)
    """The HasTraits object whose trait we look at to set the page icon"""

    icon_object_trait = Str
    """The name of the *icon_object* trait that signals an icon change"""

    
    deletable = Bool(False)
    """If the notebook has "delete" buttons, can this page be deleted?"""

    deletable_object = Instance(HasTraits)
    """
    The HasTraits object whose trait we look at to set the delete button
    enabled or disabled
    """
    
    deletable_object_trait = Str
    """The name of the *deletable_object* trait that signals a deletable change"""

    parent = Property
    """The parent window for the client page"""

    #-- Traits for use by the Notebook ----------------------------------------

    is_open = Bool(False)
    """The current open status of the notebook page"""

    min_size = Property
    """The minimum size for the page"""


    #-- Private Traits -------------------------------------------------------

    # The notebook this page is associated with:
    notebook = Instance('VerticalNotebook')

    # The control representing the open page:
    control = Property
    
    # The layout for the controls
    layout = Instance(QtGui.QVBoxLayout)
    
    # the control representing the command button.  need to keep it around
    # so we can update its name, desc, and icon dynamaically
    cmd_button = Instance(QtGui.QCommandLinkButton)
    
    # the control representing the "delete" button, if the notebook has them
    del_button = Instance(QtGui.QPushButton)

    #-- Public Methods -------------------------------------------------------


    def dispose(self):
        """ Removes this notebook page. """
 
        if self.name_object is not None:
            self.name_object.on_trait_change(self._name_updated,
                                             self.name_object_trait,
                                             remove=True)
            self.name_object = None
 
        if self.description_object is not None:
            self.description_object.on_trait_change(self._description_updated,
                                                    self.description_object_trait,
                                                    remove=True)
            
        if self.icon_object is not None:
            self.icon_object.on_trait_change(self._icon_updated,
                                             self.icon_object_trait,
                                             remove = True)


        # make sure we dispose of the child ui properly
        if self.ui is not None:
            self.ui.dispose()
            self.ui = None

        # this cleans up all the widgets in this control's layout
        self.control.deleteLater()

    def register_name_listener(self, model, trait):
        """ 
        Registers a listener on the specified object trait for a page name change.
        """
        # Save the information, so we can unregister it later:
        self.name_object, self.name_object_trait = model, trait

        # Register the listener:
        self.name_object.on_trait_change(self._name_updated, trait)

        # Make sure the name gets initialized:
        self._name_updated()

    def register_description_listener(self, model, trait):
        """
        Registers a listener on the specified object trait for a page 
        description change
        """

        # save the info so we can unregister it later
        self.description_object, self.description_object_trait = model, trait

        # register the listener
        self.description_object.on_trait_change(
            self._description_updated, trait)

        # make sure the description gets initialized
        self._description_updated()
        
    def register_icon_listener(self, model, trait):
        """
        Registers a listener on the specified object trait for a page icon
        change
        """
        
        # save the info so we can unregister it later
        self.icon_object, self.icon_object_trait = model, trait
        
        # register the listener
        self.icon_object.on_trait_change(self._icon_updated, trait)
        
        # make sure the icon gets initialized
        self._icon_updated()
        
    def register_deletable_listener(self, model, trait):
        """
        Registers a listener on the specified object trait for the delete
        button enable/disable
        """
        
        # save the info so we can unregister it later
        self.deletable_object, self.deletable_object_trait = model, trait
        
        # register the listener
        self.deletable_object.on_trait_change(self._deletable_updated, trait)
        
        # make sure the bool gets initialized
        self._deletable_updated()

    def _handle_page_toggle(self):
        if self.is_open:
            self.notebook.close(self)
        else:
            self.notebook.open(self)


    def _handle_close_button(self):
        # because of the various handlers, all we have to do is remove
        # self.data from the underlying list, and the ui should take care
        # of itself.
        self.notebook.editor.value.remove(self.data)
    
    @cached_property
    def _get_control(self):
        """ 
        Returns the control cluster for the notebook page
        """
        self.layout = QtGui.QVBoxLayout()        
        control = QtGui.QWidget()
        dpi = control.physicalDpiX()

        buttons_layout = QtGui.QHBoxLayout()
        buttons_container = QtGui.QWidget()
        
        self.cmd_button = QtGui.QCommandLinkButton(buttons_container)

        self.cmd_button.setVisible(True)
        self.cmd_button.setCheckable(True)
        self.cmd_button.setFlat(True)
        self.cmd_button.setAutoFillBackground(True)
        self.cmd_button.clicked.connect(self._handle_page_toggle)
        
        self.cmd_button.setText(self.name)
        self.cmd_button.setDescription(self.description)
        self.cmd_button.setIcon(ImageResource('ok').create_icon())
        self.cmd_button.setIconSize(QtCore.QSize(dpi * 0.2, dpi * 0.2))
        
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                                        QtGui.QSizePolicy.Preferred)
        size_policy.setHeightForWidth(True)
        self.cmd_button.setSizePolicy(size_policy)

        buttons_layout.addWidget(self.cmd_button)
        
        if self.notebook.delete:
            self.del_button = QtGui.QPushButton(buttons_container)
            self.del_button.setVisible(True)
            self.del_button.setFlat(True)
            self.del_button.setEnabled(self.deletable)
            
            self.del_button.setIcon(ImageResource('close').create_icon())
            self.del_button.setIconSize(QtCore.QSize(dpi * 0.1, dpi * 0.1))
            
            self.del_button.clicked.connect(self._handle_close_button)
            buttons_layout.addWidget(self.del_button)
            
        buttons_container.setLayout(buttons_layout)
        
        self.layout.addWidget(buttons_container)
        
        self.ui.control.setVisible(self.is_open)
        self.layout.addWidget(self.ui.control)
        
        separator = QtGui.QFrame(control)
        separator.setFrameShape(QtGui.QFrame.HLine)
        separator.setFrameShadow(QtGui.QFrame.Sunken)
        self.layout.addWidget(separator)
        
        self.layout.setContentsMargins(11, 0, 5, 0)
        control.setLayout(self.layout)
        return control

    def _get_parent(self):
        """ 
        Returns the parent window for the client's window.
        """
        return self.notebook.control

    @on_trait_change('is_open', dispatch = 'ui')
    def _on_is_open_changed(self, is_open):
        """ 
        Handles the 'is_open' state of the page being changed.
        """

        self.ui.control.setVisible(is_open)
        self.cmd_button.setChecked(is_open)
        
        if self.icon_object is None:
            if is_open:
                self.icon = 'down'
            else:
                self.icon = 'right'
                
    @on_trait_change('name', dispatch = 'ui')
    def _on_name_changed(self, name):
        """ 
        Handles the name trait being changed.
        """
        if self.cmd_button:
            self.cmd_button.setText(name)

    @on_trait_change('description', dispatch = 'ui')
    def _on_description_changed(self, description):
        if self.cmd_button:
            self.cmd_button.setDescription(description)

    @on_trait_change('icon', dispatch = 'ui')
    def _on_icon_changed(self, icon):
        if self.cmd_button:
            self.cmd_button.setIcon(ImageResource(icon).create_icon())
        
    @on_trait_change('deletable', dispatch = 'ui')
    def _on_deletable_changed(self, deletable):
        if self.del_button:
            self.del_button.setEnabled(deletable)
        
    def _name_updated(self):
        """ 
        Handles a signal that the associated object's page name has changed.
        """
        nb = self.notebook
        handler_name = None

        method = None
        editor = nb.editor
        if editor is not None:
            # I don't 100% understand this magic (taken from the wx themed 
            # vertical notebook).  looks like a handler redirect?
            method = getattr(editor.ui.handler,
                             '%s_%s_page_name' % 
                             (editor.object_name, editor.name), 
                             None)
        if method is not None:
            handler_name = method(editor.ui.info, self.name_object)

        if handler_name is not None:
            self.name = handler_name
        else:
            self.name = getattr(self.name_object,
                                self.name_object_trait) or '???'

    def _description_updated(self):
        """
        Handles the signal that the associated object's description has changed.
        """
        nb = self.notebook
        handler_desc = None

        method = None
        editor = nb.editor
        if editor is not None:
            method = getattr(editor.ui.handler,
                             '%s_%s_page_description' %
                             (editor.object_name, editor.name),
                             None)
        if method is not None:
            handler_desc = method(editor.ui.info, self.description_object)

        if handler_desc is not None:
            self.description = handler_desc
        else:
            self.description = getattr(self.description_object,
                                       self.description_object_trait) or ''
                                       
    def _icon_updated(self):
        """
        Handles the signal that the associated object's icon has changed.
        """
        nb = self.notebook
        handler_icon = None
         
        method = None
        editor = nb.editor
        if editor is not None:
            method = getattr(editor.ui.handler,
                             '%s_%s_page_icon' % 
                             (editor.object_name, editor.name),
                             None)
         
        if method is not None:
            handler_icon = method(editor.ui.info, self.icon_object)
             
        if handler_icon is not None:
            self.icon = handler_icon
        else:
            self.icon = getattr(self.icon_object, self.icon_object_trait, None)

    def _deletable_updated(self):
        """
        Handles the signal that the associated object's deletable state has changed.
        """
        nb = self.notebook
        handler_deletable = None
         
        method = None
        editor = nb.editor
        if editor is not None:
            method = getattr(editor.ui.handler,
                             '%s_%s_page_deletable' % 
                             (editor.object_name, editor.name),
                             None)
         
        if method is not None:
            handler_deletable = method(editor.ui.info, self.deletable_object)
             
        if handler_deletable is not None:
            self.deletable = handler_deletable
        else:
            self.deletable = getattr(self.deletable_object, self.deletable_object_trait, False)


#-------------------------------------------------------------------------
#  'VerticalNotebook' class:
#-------------------------------------------------------------------------


class VerticalNotebook(HasPrivateTraits):
    """ 
    Defines a ThemedVerticalNotebook class for displaying a series of pages
    organized vertically, as opposed to horizontally like a standard notebook.
    """

    #-- Public Traits --------------------------------------------------------

    multiple_open = Bool(False)
    """Allow multiple open pages at once?"""

    
    delete = Bool(False)
    """can the editor delete list items?"""

    pages = List(VerticalNotebookPage)
    """The pages contained in the notebook"""

    editor = Instance(Editor)
    """The traits UI editor this notebook is associated with (if any)"""

    #-- Private Traits -------------------------------------------------------

    # The Qt control used to represent the notebook:
    control = Instance(QtGui.QWidget)

    # The Qt layout containing the child widgets & layouts
    layout = Instance(QtGui.QVBoxLayout)

    #-- Public Methods -------------------------------------------------------

    def create_control(self, parent):
        """ 
        Creates the underlying Qt window used for the notebook.
        """

        self.layout = QtGui.QVBoxLayout()
        self.control = QtGui.QWidget()
        self.control.setLayout(self.layout)

        return self.control

    def create_page(self):
        """ 
        Creates a new **VerticalNotebook** object representing a notebook page and
        returns it as the result.
        """
        return VerticalNotebookPage(notebook=self)

    def open(self, page):
        """ 
        Handles opening a specified notebook page.
        """
        if (page is not None) and (not page.is_open):
            if not self.multiple_open:
                for a_page in self.pages:
                    a_page.is_open = False

            page.is_open = True

    def close(self, page):
        """ 
        Handles closing a specified notebook page.
        """
        if (page is not None) and page.is_open:
            page.is_open = False

    #-- Trait Event Handlers -------------------------------------------------

    def _pages_changed(self, old, new):
        """ 
        Handles the notebook's pages being changed.
        """
        for page in old:
            page.dispose()

        self._refresh()

    def _pages_items_changed(self, event):
        """ 
        Handles some of the notebook's pages being changed.
        """
        for page in event.removed:
            page.dispose()

        self._refresh()

    def _multiple_open_changed(self, multiple_open):
        """ 
        Handles the 'multiple_open' flag being changed.
        """
        if not multiple_open:
            first = True
            for page in self.pages:
                if first and page.is_open:
                    first = False
                else:
                    page.is_open = False

    #-- Private Methods ------------------------------------------------------

    def _refresh(self):
        """ 
        Refresh the layout and contents of the notebook.
        """

        self.control.setUpdatesEnabled(False)

        while self.layout.count() > 0:
            self.layout.takeAt(0)

        for page in self.pages:
            self.layout.addWidget(page.control)
            
        self.layout.addStretch(1)
        self.control.setUpdatesEnabled(True)


if __name__ == '__main__':

    from traitsui.api import View, Group, Item
    from cytoflowgui.editors.vertical_notebook_editor import VerticalNotebookEditor

    class TestPageClass(HasTraits):
        trait1 = Str
        trait2 = Bool
        trait3 = Bool

        traits_view = View(Group(Item(name='trait1'),
                                 Item(name='trait2'),
                                 Item(name='trait3')))

    class TestList(HasTraits):
        el = List(TestPageClass)

        view = View(
            Group(
                Item(name='el',
                     id='table',
                     #editor = ListEditor()
                     editor=VerticalNotebookEditor(page_name='.trait1',
                                                   view='traits_view',
                                                   delete = True)
                     )),
                    resizable = True)

    from cytoflowgui.utility import record_events 
    import os
            
    with record_events() as container:
        test = TestList()
        test.el.append(TestPageClass(trait1="one", trait2=True))
        test.el.append(TestPageClass(trait1="three", trait2=False))
        
        test.configure_traits()
    container.save_to_directory(os.getcwd())

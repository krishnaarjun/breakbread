import Vue from 'vue'
var dragDropHandles = {
  handleDragStart: function (e) {
    e.target.classList.add('dragging')
    e.dataTransfer.effectAllowed = 'move'
    // Need to set to something or else drag doesn't start
    e.dataTransfer.setData('text', '*')
    this.vnode.context.$emit('drag-start')
  }.bind(this),
  handleDragOver: function (e) {
    if (e.preventDefault) {
      e.preventDefault()
    }

    e.dataTransfer.dropEffect = 'move'
    e.target.classList.add('drag-over')
    this.vnode.context.$emit('drag-over')

    return false
  },
  handleDragEnter: function (e) {
    this.vnode.context.$emit('drag-enter')
    e.target.classList.add('drag-enter')
  },
  handleDragLeave: function (e) {
    this.vnode.context.$emit('drag-leave')
    e.target.classList.remove('drag-enter', 'drag-over')
  },
  handleDrag: function (e) {
    this.vnode.context.$emit('drag')
  },
  handleDragEnd: function (e) {
    e.target.classList.remove('dragging', 'drag-over', 'drag-enter')
    this.vnode.context.$emit('drag-end')
  },
  handleDrop: function (e) {
    e.preventDefault()
    if (e.stopPropagation) {
      // stops the browser from redirecting.
      e.stopPropagation()
    }

    // Don't do anything if dropping the same column we're dragging.
    this.vnode.context.$emit('drop')

    return false
  }
}
Vue.directive('drag-drop', {
  bind (el, binding, vnode) {
    dragDropHandles.el = el
    dragDropHandles.binding = binding
    dragDropHandles.vnode = vnode
    // this.handleDragStart = e => {
    //   e.target.classList.add("dragging");
    //   e.dataTransfer.effectAllowed = "move";
    //   // Need to set to something or else drag doesn't start
    //   e.dataTransfer.setData("text", "*");
    //   vnode.context.$emit("drag-start");
    // };

    // this.handleDragOver = e => {
    //   if (e.preventDefault) {
    //     e.preventDefault();
    //   }

    //   e.dataTransfer.dropEffect = "move";
    //   e.target.classList.add("drag-over");
    //   vnode.context.$emit("drag-over");

    //   return false;
    // };

    // this.handleDragEnter = e => {
    //   vnode.context.$emit("drag-enter");
    //   e.target.classList.add("drag-enter");
    // };

    // this.handleDragLeave = e => {
    //   vnode.context.$emit("drag-leave");
    //   e.target.classList.remove("drag-enter", "drag-over");
    // };

    // this.handleDrag = e => {
    //   vnode.context.$emit("drag");
    // };

    // this.handleDragEnd = e => {
    //   e.target.classList.remove("dragging", "drag-over", "drag-enter");
    //   vnode.context.$emit("drag-end");
    // };

    // this.handleDrop = e => {
    //   e.preventDefault();
    //   if (e.stopPropagation) {
    //     // stops the browser from redirecting.
    //     e.stopPropagation();
    //   }

    //   // Don't do anything if dropping the same column we're dragging.
    //   vnode.context.$emit("drop");

    //   return false;
    // };

    // setup the listeners
    el.setAttribute('draggable', 'true')
    el.addEventListener('dragstart', dragDropHandles.handleDragStart, false)
    el.addEventListener('dragenter', dragDropHandles.handleDragEnter, false)
    el.addEventListener('dragover', dragDropHandles.handleDragOver, false)
    el.addEventListener('drag', dragDropHandles.handleDrag, false)
    el.addEventListener('dragleave', dragDropHandles.handleDragLeave, false)
    el.addEventListener('dragend', dragDropHandles.handleDragEnd, false)
    el.addEventListener('drop', dragDropHandles.handleDrop, false)
  },
  unbind (el) {
    // Called when element is being removed
    el.classList.remove('dragging', 'drag-over', 'drag-enter')
    el.removeAttribute('draggable')
    el.removeEventListener('dragstart', dragDropHandles.handleDragStart)
    el.removeEventListener('dragenter', dragDropHandles.handleDragEnter)
    el.removeEventListener('dragover', dragDropHandles.handleDragOver)
    el.removeEventListener('dragleave', dragDropHandles.handleDragLeave)
    el.removeEventListener('drag', dragDropHandles.handleDrag)
  }
})

Vue.component('users-view', {
  data: function () {
    return {
      gridInstance: null,
      users: [],
      search: '',
      isNewUserModal: true,
      showModalContent: false,
      username: '',
      roleValue: [],
      roleOptions: [
        {
          id: "manage_users",
          text: "Manage users",
        },
        {
          id: "view_archive",
          text: "View archive",
        },
      ],
      queueValue: [],
      queueOptions: [
        {
          id: "global",
          text: "Global",
        },
        {
          id: "secondary",
          text: "Secondary",
        },
      ],
    }
  },
  methods: {
    getUsers () {
      return new Promise(resolve => {
        fetch('https://my-json-server.typicode.com/burhanahmeed/sunnah-com-mock/users', {
          method: 'GET'
        })
        .then(response => response.json())
        .then(response => {
          console.log(response);
          this.users = response;
          // this.reloadData();
          resolve(response);
        })
      })
    },
    handleAddUserModal () {
      $('#add-user-modal').modal();
      this.username = '';
      this.roleValue = []
      this.queueValue = [];
      this.showModalContent = true;
    },
    handleEditUser (selectedUser = {}) {
      this.username = selectedUser.username;
      if (selectedUser.permissions.manage_users) {
        this.roleValue.push('manage_users');
      };
      if (selectedUser.permissions.view_archive) {
        this.roleValue.push('view_archive');
      }
      this.queueValue = selectedUser.permissions.queues;
      this.isNewUserModal = false;
      this.showModalContent = true;
      $('#add-user-modal').modal('show');
    },
    closeModal () {
      this.isNewUserModal = true;
      this.showModalContent = false;
      this.username = '';
      this.roleValue = []
      this.queueValue = [];
      $('#add-user-modal').modal('hide');
    },
    handleDelete () {
      if (confirm('Are you sure want to delete this user?')) {
        console.log('deleted!');
      }
    }
  },
  computed: {
    usersData () {
      let users = this.users;
      users = users.filter(el => {
        if (el.username.toLowerCase().indexOf(this.search.toLowerCase()) != -1) {
          return true;
        } 
      });
      return users;
    }
  },
  mounted: async function () {
    await this.getUsers();
    const vm = this;
    $('#add-user-modal').on('hidden.bs.modal', function (event) {
      vm.closeModal();
    })
    
  }
})

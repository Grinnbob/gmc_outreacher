import DashboardLayout from 'src/pages/Dashboard/Layout/DashboardLayout.vue'
// GeneralViews
import NotFound from 'src/pages/GeneralViews/NotFoundPage.vue'
// Dashboard pages
import Overview from 'src/pages/Dashboard/Dashboard/Overview.vue'
import Stats from 'src/pages/Dashboard/Dashboard/Stats.vue'

// Pages
import User from 'src/pages/Dashboard/Pages/UserProfile.vue'
import TimeLine from 'src/pages/Dashboard/Pages/TimeLinePage.vue'
import Login from 'src/pages/Dashboard/Pages/Login.vue'
import Register from 'src/pages/Dashboard/Pages/Register.vue'
import Lock from 'src/pages/Dashboard/Pages/Lock.vue'


// Components pages
import Buttons from 'src/pages/Dashboard/Components/Buttons.vue'
import GridSystem from 'src/pages/Dashboard/Components/GridSystem.vue'
import Panels from 'src/pages/Dashboard/Components/Panels.vue'
const SweetAlert = () => import('src/pages/Dashboard/Components/SweetAlert.vue')
import Notifications from 'src/pages/Dashboard/Components/Notifications.vue'
import Icons from 'src/pages/Dashboard/Components/Icons.vue'
import Typography from 'src/pages/Dashboard/Components/Typography.vue'

// Forms pages
const RegularForms = () => import('src/pages/Dashboard/Forms/RegularForms.vue')
const ExtendedForms = () => import('src/pages/Dashboard/Forms/ExtendedForms.vue')
const ValidationForms = () => import('src/pages/Dashboard/Forms/ValidationForms.vue')
const Wizard = () => import('src/pages/Dashboard/Forms/Wizard.vue')

// TableList pages
const RegularTables = () => import('src/pages/Dashboard/Tables/RegularTables.vue')
const ExtendedTables = () => import('src/pages/Dashboard/Tables/ExtendedTables.vue')
const PaginatedTables = () => import('src/pages/Dashboard/Tables/PaginatedTables.vue')



// Charts
const Charts = () => import('src/pages/Dashboard/Charts.vue')

//CUSTOM components created by me
const Prospects = () => import('src/pages/Dashboard/Prospects/prospects.vue')
const CampaignWizard = () => import('src/pages/Dashboard/Campaigns/campaignWizard.vue')
const Campaign = () => import('src/pages/Dashboard/Campaigns/campaign.vue')
const Campaigns = () => import('src/pages/Dashboard/Campaigns/campaigns.vue')

const CampaignsList = () => import('src/pages/Dashboard/CampaignsList/campaigns.vue')
const CampaignForm = () => import('src/pages/Dashboard/CampaignsList/campaign_form.vue')
const CampaignEditForm = () => import('src/pages/Dashboard/CampaignsList/campaign_edit_form.vue')


const Statistics = () => import('src/pages/Dashboard/Statistics/statistics.vue')
const Statistics_detailed = () => import('src/pages/Dashboard/Statistics/statistics_detailed.vue')


const Accounts = () => import('src/pages/Dashboard/Accounts/accounts.vue')
const Team = () => import('src/pages/Dashboard/Team/team.vue')
const Actions = () => import('src/pages/Dashboard/Actions/actions.vue')

const test_json_campaign = () => import('src/pages/Dashboard/Campaigns/test_json_from_server.vue')


const filterForm = () => import('src/pages/Dashboard/TestComponents/formComponent.vue')
const randomComponent = () => import('src/pages/Dashboard/TestComponents/randomComponent.vue')

let componentsMenu = {
  path: '/components',
  component: DashboardLayout,
  redirect: '/components/buttons',
  children: [
    {
      path: 'buttons',
      name: 'Buttons',
      component: Buttons
    },
    {
      path: 'grid-system',
      name: 'Grid System',
      component: GridSystem
    },
    {
      path: 'panels',
      name: 'Panels',
      component: Panels
    },
    {
      path: 'sweet-alert',
      name: 'Sweet Alert',
      component: SweetAlert
    },
    {
      path: 'notifications',
      name: 'Notifications',
      component: Notifications
    },
    {
      path: 'icons',
      name: 'Icons',
      component: Icons
    },
    {
      path: 'typography',
      name: 'Typography',
      component: Typography
    }

  ]
}

let testComponents = {
  path: '/test',
  component: DashboardLayout,
  redirect: '/test/1',
  children: [
    {
      path: '1',
      name: 'Filter Form',
      component: filterForm
    },
    {
      path: '2',
      name: 'Random component',
      component: randomComponent
    },
  ]
}


let formsMenu = {
  path: '/forms',
  component: DashboardLayout,
  redirect: '/forms/regular',
  children: [
    {
      path: 'regular',
      name: 'Regular Forms',
      component: RegularForms
    },
    {
      path: 'extended',
      name: 'Extended Forms',
      component: ExtendedForms
    },
    {
      path: 'validation',
      name: 'Validation Forms',
      component: ValidationForms
    },
    {
      path: 'wizard',
      name: 'Wizard',
      component: Wizard
    }
  ]
}

let tablesMenu = {
  path: '/table-list',
  component: DashboardLayout,
  redirect: '/table-list/regular',
  children: [
    {
      path: 'regular',
      name: 'Regular Tables',
      component: RegularTables
    },
    {
      path: 'extended',
      name: 'Extended Tables',
      component: ExtendedTables
    },
    {
      path: 'paginated',
      name: 'Paginated Tables',
      component: PaginatedTables
    }]
}


let pagesMenu = {
  path: '/pages',
  component: DashboardLayout,
  redirect: '/pages/user',
  children: [
    {
      path: 'user',
      name: 'User Page',
      component: User
    },
    {
      path: 'timeline',
      name: 'Timeline Page',
      component: TimeLine
    }
  ]
}

let loginPage = {
  path: '/login',
  name: 'Login',
  component: Login
}

let registerPage = {
  path: '/register',
  name: 'Register',
  component: Register
}

let lockPage = {
  path: '/lock',
  name: 'Lock',
  component: Lock
}


const routes = [
  {
    path: '/',
    redirect: '/admin/overview'
  },
  componentsMenu,
  testComponents,
  formsMenu,
  tablesMenu,
  pagesMenu,
  loginPage,
  registerPage,
  lockPage,
  {
    path: '/admin',
    component: DashboardLayout,
    redirect: '/admin/overview',
    children: [
      {
        path: 'overview',
        name: 'Overview',
        component: Overview
      },
      {
        path: 'stats',
        name: 'Stats',
        component: Stats
      },
      {
        path: 'charts',
        name: 'Charts',
        component: Charts
      },
      {
        path: 'prospects',
        name: 'Prospects',
        component: Prospects
      },
      {
        path: 'campaignWizard',
        name: 'CampaignWizard',
        component: CampaignWizard
      },
      {
        path: 'campaigns',
        name: 'Campaigns',
        component: Campaigns
      },
      {
        path: 'campaigns_new',
        name: 'CampaignsList',
        component: CampaignsList
      },
      {
        path: 'campaign_form',
        name: 'CampaignForm',
        component: CampaignForm
      },
      {
        path: 'campaign_edit_form',
        name: 'CampaignEditForm',
        component: CampaignEditForm
      },

      {
        path: 'campaign',
        name: 'Campaign',
        component: Campaign
      },
      {
        path: 'campaigns_test_json',
        name: 'Campaigns TEST JSON',
        component: test_json_campaign
      },
      {
        path: 'accounts',
        name: 'Accounts',
        component: Accounts
      },
      {
        path: 'team',
        name: 'Team',
        component: Team
      },
      {
        path: 'actions',
        name: 'Actions',
        component: Actions
      },
      {
        path: 'statistics',
        name: 'Statistics',
        component: Statistics
      },
      {
        path: 'statistics_detailed',
        name: 'Statistics_detailed',
        component: Statistics_detailed
      }
    ]
  },
  {path: '*', component: NotFound}
]

export default routes

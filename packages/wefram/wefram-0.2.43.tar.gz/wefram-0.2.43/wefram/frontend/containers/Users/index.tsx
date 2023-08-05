import React, {createRef} from 'react'
import {
  Box,
  Dialog,
  EntityList,
  MaterialIcon, MenuButton,
  Typography
} from 'system/components'
import {ScreenProps} from 'system/types'
import {gettext} from 'system/l10n'
import {api} from 'system/api'
import {RequestApiPath} from 'system/routing'
import User from '../User'


const objectsPath: RequestApiPath = api.entityPath('system', 'User')


type ScreenState = {
  entityKey?: string | null
}


export default class Screen extends React.Component<ScreenProps> {
  state: ScreenState = {
    entityKey: undefined
  }

  private listRef = createRef<EntityList>()

  render() {
    return (
      <React.Fragment>
      <Box mt={1}>
        <Typography variant={'h4'} paddingBottom={2}>
          {gettext("Administrate users", 'system.aaa')}
        </Typography>
        <EntityList
          ref={this.listRef}

          addButtonAction={() => this.setState({entityKey: null})}
          avatarColor
          avatarField={'avatar'}
          controls={[
            <MenuButton
              variant={'outlined'}
              items={[
                {
                  icon: 'lock',
                  iconColor: 'red',
                  caption: gettext('Lock selected', 'system.aaa'),
                  onClick: () => {}
                },
                {
                  icon: 'lock_open',
                  caption: gettext('Unlock selected', 'system.aaa'),
                  onClick: () => {}
                }
              ]}
            />
          ]}
          defaultSort={{value: 'fullName', direction: 'asc'}}
          deleteButton={true}
          deleteConfirmMessage={gettext("Are you sure you want to delete the selected users?", 'system.aaa-messages')}
          entityCaption={gettext("Users list", 'system.aaa')}
          limit={30}
          pagination
          primaryField={'fullName'}
          requestPath={objectsPath}
          sortOptions={[
            {value: 'login', caption: gettext("Login", 'system.aaa-list')},
            {value: 'fullName', caption: gettext("Full name", 'system.aaa-list')}
          ]}
          search
          secondaryField={[
            [
              {
                fieldType: 'boolean',
                fieldName: 'locked',
                hidden: (value: any): boolean => !Boolean(value),
                valueVisualize: (value: any): any => {
                  return value
                    ? (<MaterialIcon icon={'lock'} size={20} color={'red'} />)
                    : (<MaterialIcon icon={'lock_open'} size={20} color={'grey'} />)
                }
              },
              'login',
            ],
            {
              fieldType: 'dateTimeNice',
              fieldName: 'lastLogin',
              caption: gettext("Last logged on", 'system.aaa-list')
            }
          ]}
          selectable
          storageEntity={'system.users'}
          textTotalCount
          variant={'cards'}
          urlStateOffset
          urlStateSearch
          onItemClick={(item: any) => {
            this.setState({entityKey: item.id})
          }}
        />
      </Box>
      <Dialog open={this.state.entityKey !== undefined} maxWidth={'sm'}>
        {this.state.entityKey !== undefined && (
          <User
            entityKey={this.state.entityKey}
            onClose={() => {
              this.setState({entityKey: undefined})
            }}
            onAfterDelete={() => {
              this.listRef.current?.update()
              this.setState({entityKey: undefined})
            }}
            onAfterSubmit={() => {
              this.listRef.current?.update()
              this.setState({entityKey: undefined})
            }}
          />
        )}
      </Dialog>
      </React.Fragment>
    )
  }
}

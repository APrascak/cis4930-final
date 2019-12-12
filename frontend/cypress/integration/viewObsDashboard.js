describe('View OBS dashboard', function() {
    context('Actions', () => {
	beforeEach(() => {
        cy.visit('http://localhost:3000/account')
	})

	it('Attempts to sign in user and see dashboard', () => {
        //user signs in and is able to see their dashboard
        cy.visit('http://localhost:3000/signin')
        cy.get('input[name="email"]').type('qwerty@mail.com')
        cy.get('input[name="password"]').type('password')
        cy.get('button').should('be.enabled')
        cy.get('form').submit()
        cy.visit('http://localhost:3000/account')
		
        cy.location('pathname').should('eq', '/account')
        
    })
    
})
})


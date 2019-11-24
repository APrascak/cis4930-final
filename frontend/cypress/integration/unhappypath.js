
describe('Unhappy Path Test', function() {
    it('Tests signup', function() {
        var num = (Math.random()*10)

        cy.visit('http://localhost:3000/signup')

        cy.get('#username')
        .type('test')
        .should('have.value', 'test')

        cy.get('#email')
        .type(('testing'+ num + '@email.com'))
        .should('have.value', ('testing'+ num + '@email.com'))

        cy.get('#passwordOne')
        .type('test')
        .should('have.value', 'test')

        cy.get('#passwordTwo')
        .type('test')
        .should('have.value', 'test')

        cy.get('form').submit()
        cy.url().should('not.include', '/home')

    })
})
